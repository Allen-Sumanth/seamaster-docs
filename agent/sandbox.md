There's two snippets in this file
1. Config (infer timeouts and all here)
2. Game Loop (infer data about the game loop here)

```go
func New() *Config {
        isProd := os.Getenv("PROD") == "true"

        return &Config{
                IsProd:               isProd,
                MaxConcurrentMatches: getEnv("MAX_CONCURRENT_MATCHES", 10),

                MatchJobQueueConfig: MatchJobQueueConfig{
                        URL:          getEnv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672"),
                        ExchangeName: getEnv("RABBITMQ_EXCHANGE", "match_jobs"),
                        QueueName:    getEnv("RABBITMQ_QUEUE", "match_jobs"),
                        RoutingKey:   getEnv("RABBITMQ_ROUTING_KEY", "match_jobs"),
                },

                NsjailPath:    "/app/nsjail",
                NsjailCfgPath: "/app/nsjail.cfg",

                WrapperPyPath:      "/wrapper.py",
                HostSubmissionPath: "/submissions",

                JailSubmissionPath:    "/submission",
                JailHostname:          "jail",
                JailCwd:               "/",
                JailCGroupPidsMax:     20,                // 20 processes
                JailCGroupMemMax:      100 * 1024 * 1024, // 100 MB
                JailCGroupCpuMsPerSec: 200,               // 20% CPU
                JailTmpfsSize:         100 * 1024 * 1024, // 100 MB

                // Wall >= Setup + 1000 * Tick
                JailWallTimeoutMS:      2 * 60 * 1000, // 2 minutes
                JailHandshakeTimeoutMS: 30 * 1000,     // 30 seconds
                JailTickTimeoutMS:      2000,          // 2 seconds
        }
}```


```go
package engine

import (
        "context"
        "fmt"
        "strings"
        "time"

        "github.com/delta/code-runner/internal/config"
        "github.com/delta/code-runner/internal/sandbox"
)

const (
        HANDSHAKE_MSG     = "__READY_V1__"
        MAX_TIMEOUT_COUNT = 5
)

type Match struct {
        ID         int
        Player1    int
        Player2    int
        Player1Dir string
        Player2Dir string
        gl         *GameLogger
}

func NewMatch(id, p1, p2 int, p1Dir, p2Dir string, gl *GameLogger) *Match {
        return &Match{
                ID:         id,
                Player1:    p1,
                Player2:    p2,
                Player1Dir: p1Dir,
                Player2Dir: p2Dir,
                gl:         gl,
        }
}


// Results:
// If ticks is 1000, the match is OK. just use the winner field. -1 if draw (equal algae)
// The problem is when ticks is less than 1000, the match is not OK. The winner field is not reliable.
// Make use of the algae count, time taken by the players and consecutive timeouts to determine the winner.
type MatchResults struct {
        Winner     int      `json:"winner"`      // Winner ID if someone won, -1 if draw or early exit
        Ticks      int      `json:"ticks"`       // Tick number at the end of the match
        MaxAlgae   int      `json:"max_algae"`   // Maximum algae count during the match
        AlgaeCnt   [2]int   `json:"algae_cnt"`   // Algae count at the end of the match
        TimeTaken  [2]int64 `json:"time_taken"`  // Time consumed by each player (cumulative of all ticks)
        TimeoutCnt [2]uint  `json:"timeout_cnt"` // Number of consecutive timeouts of each player
}

// returned error is also logged to gameLog file by the manager
func (m *Match) Simulate(cfg *config.Config) (*MatchResults, error) {
        m.gl.Log(GameLogDebug, "Starting sandbox")

        matchCtx, cancelCtx := context.WithTimeout(context.Background(), time.Duration(cfg.JailWallTimeoutMS)*time.Millisecond)
        defer cancelCtx()

        s1, err := sandbox.NewSandbox(matchCtx, cfg.NsjailPath, cfg.NsjailCfgPath, m.Player1Dir, cfg.JailSubmissionPath)
        if err != nil {
                return nil, fmt.Errorf("create p1 sandbox: %w", err)
        }
        defer s1.Destroy()

        s2, err := sandbox.NewSandbox(matchCtx, cfg.NsjailPath, cfg.NsjailCfgPath, m.Player2Dir, cfg.JailSubmissionPath)
        if err != nil {
                return nil, fmt.Errorf("create p2 sandbox: %w", err)
        }
        defer s2.Destroy()

        go streamErrors(matchCtx, s1, m.gl, "p1")
        go streamErrors(matchCtx, s2, m.gl, "p2")

        if err := s1.Start(); err != nil {
                return nil, fmt.Errorf("start p1 sandbox: %w", err)
        }
        if err := s2.Start(); err != nil {
                return nil, fmt.Errorf("start p2 sandbox: %w", err)
        }

        if err := handshakeSandbox(matchCtx, s1, cfg.JailHandshakeTimeoutMS); err != nil {
                return nil, fmt.Errorf("p1 handshake: %w", err)
        }

        if err := handshakeSandbox(matchCtx, s2, cfg.JailHandshakeTimeoutMS); err != nil {
                return nil, fmt.Errorf("p2 handshake: %w", err)
        }

        m.gl.Log(GameLogDebug, "Completed Handshakes")

        var (
                ge                 = InitGameEngine(m.gl)
                p1Time       int64 = 0
                p2Time       int64 = 0
                p1TimeoutCnt uint  = 0 // consecutive errors
                p2TimeoutCnt uint  = 0
        )

        for {
                isP1Turn := ge.Ticks%2 == 1

                m.gl.Log(GameLogGameView, ge.getGameView())

                turnCtx, cancelTurnCtx := context.WithTimeout(matchCtx, time.Duration(cfg.JailTickTimeoutMS)*time.Millisecond)

                move := PlayerMoves{}
                var turnErr error

                start := time.Now()
                if isP1Turn {
                        turnErr = doTurn(turnCtx, s1, m.gl, "p1", ge.GetPlayerView(PlayerOne), &move)
                        p1Time += time.Since(start).Milliseconds()
                } else {
                        turnErr = doTurn(turnCtx, s2, m.gl, "p2", ge.GetPlayerView(PlayerTwo), &move)
                        p2Time += time.Since(start).Milliseconds()
                }

                cancelTurnCtx()

                if turnErr != nil {
                        // skip turn and wait till MAX_TIMEOUT_COUNT consecutive turn errors to end the match?
                        if isP1Turn {
                                m.gl.Log(GameLogError, "p1", turnErr)
                                p1TimeoutCnt++
                                if p1TimeoutCnt >= MAX_TIMEOUT_COUNT {
                                        m.gl.Log(GameLogDebug, "match ended: p1 exceeded max timeouts")
                                        return &MatchResults{
                                                Winner:     -1, //draw
                                                Ticks:      ge.Ticks,
                                                MaxAlgae:   ge.AlgaeCount,
                                                AlgaeCnt:   ge.PermanentAlgae,
                                                TimeTaken:  [2]int64{p1Time, p2Time},
                                                TimeoutCnt: [2]uint{p1TimeoutCnt, p2TimeoutCnt},
                                        }, nil
                                }
                        } else {
                                m.gl.Log(GameLogError, "p2", turnErr)
                                p2TimeoutCnt++
                                if p2TimeoutCnt >= MAX_TIMEOUT_COUNT {
                                        m.gl.Log(GameLogDebug, "match ended: p2 exceeded max timeouts")
                                        return &MatchResults{
                                                Winner:     -1, //draw
                                                Ticks:      ge.Ticks,
                                                MaxAlgae:   ge.AlgaeCount,
                                                AlgaeCnt:   ge.PermanentAlgae,
                                                TimeTaken:  [2]int64{p1Time, p2Time},
                                                TimeoutCnt: [2]uint{p1TimeoutCnt, p2TimeoutCnt},
                                        }, nil
                                }
                        }
                } else {
                        if isP1Turn {
                                p1TimeoutCnt = min(p1TimeoutCnt-1, 0)
                        } else {
                                p2TimeoutCnt = min(p2TimeoutCnt-1, 0)
                        }
                        m.gl.Log(GameLogGameMove, move)
                        ge.UpdateState(move)
                }

                if ge.Winner != -1 {
                        break
                }
        }

        winner := -1
        switch ge.Winner {
        case 0:
                winner = m.Player1
        case 1:
                winner = m.Player2
        }

        return &MatchResults{
                Winner:     winner,
                Ticks:      ge.Ticks,
                MaxAlgae:   ge.AlgaeCount,
                AlgaeCnt:   ge.PermanentAlgae,
                TimeTaken:  [2]int64{p1Time, p2Time},
                TimeoutCnt: [2]uint{p1TimeoutCnt, p2TimeoutCnt},
        }, nil
}

func handshakeSandbox(mCtx context.Context, s *sandbox.Sandbox, timeoutMS uint32) error {
        ctx, cancel := context.WithTimeout(mCtx, time.Duration(timeoutMS)*time.Millisecond)
        defer cancel()

        data := ""

        err := s.RecvOutput(ctx, &data)
        if err != nil {
                return err
        }

        if strings.TrimSpace(data) != HANDSHAKE_MSG {
                return fmt.Errorf("Invalid handshake")
        }

        return nil
}

func doTurn(turnCtx context.Context, s *sandbox.Sandbox, gl *GameLogger, label string, playerView PlayerViewDTO, out *PlayerMoves) error {
        gl.Log(GameLogDebug, label, "Sending state")

        if err := s.Send(playerView); err != nil {
                return fmt.Errorf("send state: %w", err)
        }

        gl.Log(GameLogDebug, label, "Waiting for output")

        for {
                *out = PlayerMoves{}
                err := s.RecvOutput(turnCtx, out)
                if err != nil {
                        if turnCtx.Err() != nil {
                                return fmt.Errorf(
                                        "turn timed out waiting for valid output: %w",
                                        turnCtx.Err(),
                                )
                        }

                        gl.Log(GameLogWarn, label, fmt.Sprintf("Invalid output: %v", err))
                        continue
                }

                if out.Tick != playerView.Tick {
                        gl.Log(
                                GameLogWarn,
                                label,
                                fmt.Sprintf("Bad tick: got %d, expected %d", out.Tick, playerView.Tick),
                        )
                        continue
                }

                gl.Log(GameLogDebug, label, "Completed Turn")
                return nil
        }
}

func streamErrors(ctx context.Context, s *sandbox.Sandbox, gl *GameLogger, label string) {
        for {
                data, err := s.RecvError(ctx)
                if err != nil {
                        return
                }
                if strings.TrimSpace(string(data)) != "" {
                        gl.Log(GameLogError, label, string(data))
                }
        }
}
```