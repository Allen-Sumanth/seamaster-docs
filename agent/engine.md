This file has 2 snippets:
1. Engine types 
2. Engine code

```
package engine

import (
        "math/rand"
)

// Stores all information availlable in a game
type GameEngine struct {
        Ticks          int
        BotIDSeed      [2]int
        MaxBots        int
        Grid           [20][20]Tile
        AllBots        map[int]*Bot  //Map of Bot structures, key is its ID
        Scraps         [2]int        // 0 -> player A, 1 -> player B
        Banks          map[int]*Bank //key is bankID
        EnergyPads     map[int]*Pad
        PermanentAlgae [2]int
        Winner         int
        AlgaeCount     int
        Walls          []Point // Added again alongside grid for redundancy and speed
        gl             *GameLogger
}

type Bot struct {
        ID            int      `json:"id"`
        OwnerID       int      `json:"owner_id"` // 0 = Player A, 1 = Player B
        Location      Point    `json:"location"`
        Energy        float64  `json:"energy"`
        Scraps        int      `json:"scraps"`
        Abilities     []string `json:"abilities"`
        VisionRadius  int      `json:"vision_radius"`
        AlgaeHeld     int      `json:"algae_held"`
        TraversalCost float64  `json:"traversal_cost"`
        Status        string   `json:"status"`
}

var CostDB = map[string]int{
        "HARVEST":      10,
        "SCOUT":        10,
        "SELFDESTRUCT": 5,
        "LOCKPICK":     5,
        "SPEEDBOOST":   10,
        "POISON":       5,
        "SHIELD":       5,
}

var EnergyDB = map[string]EnergyCost{
        "HARVEST":      {0, 1},
        "SCOUT":        {1.5, 0}, //Pulse mechanic needs be discussed
        "SELFDESTRUCT": {0.5, 0},
        "SPEEDBOOST":   {1, 0},
        "POISON":       {0.5, 2},
        "LOCKPICK":     {1.5, 0},
        "SHIELD":       {0.25, 0},
        "DEPOSIT":      {0, 1},
        "MOVE":         {0, 0},
}

type EnergyCost struct {
        Traversal float64
        Ability   float64
}

type Tile struct {
        HasAlgae bool
        IsPoison bool
        IsWall   bool
}

type Bank struct {
        ID                int   `json:"id"`
        Location          Point `json:"location"`
        DepositOccuring   bool  `json:"deposit_occuring"`
        DepositAmount     int   `json:"deposit_amount"`
        DepositOwner      int   `json:"deposit_owner"`
        BankOwner         int   `json:"bank_owner"` //0 = player A, 1 = player B
        DepositTicksLeft  int   `json:"deposit_ticks_left"`
        LockPickOccuring  bool  `json:"lockpick_occuring"`
        LockPickTicksLeft int   `json:"lockpick_ticks_left"`
        LockPickBotID     int   `json:"lockpick_botid"`
}

type Pad struct {
        ID        int   `json:"id"`
        Location  Point `json:"location"`
        Available bool  `json:"available"`
        TicksLeft int   `json:"ticks_left"`
}

type Point struct {
        X int `json:"x"`
        Y int `json:"y"`
}

type PermanentEntities struct {
        Banks      map[int]Bank `json:"banks"`
        EnergyPads map[int]Pad  `json:"energy_pads"`
        Walls      []Point      `json:"walls"`
}

// Starts empty game engine instance
func InitGameEngine(gl *GameLogger) *GameEngine {
        ge := &GameEngine{
                Ticks:     1,
                BotIDSeed: [2]int{100, 200},
                MaxBots:   50,
                Grid:      [20][20]Tile{},
                Scraps:    [2]int{},

                AllBots:    make(map[int]*Bot),
                Banks:      make(map[int]*Bank),
                EnergyPads: make(map[int]*Pad),
                Winner:     -1,

                gl: gl,
        }
        ge.Scraps[PlayerOne] = 100
        ge.Scraps[PlayerTwo] = 100

        ge.initBanks()
        ge.initPads()
        ge.generateBoard()
        return ge
}

func (ge *GameEngine) initBanks() {
        ge.Banks[1] = initBank(1, 4, 4, PlayerOne)
        ge.Banks[2] = initBank(2, 15, 4, PlayerTwo)
        ge.Banks[3] = initBank(3, 4, 15, PlayerOne)
        ge.Banks[4] = initBank(4, 15, 15, PlayerTwo)
}

// Need to update Bank structure to have ownership of Banks(can't deposit in enemy bank)
func initBank(id int, x int, y int, playerID int) *Bank {
        return &Bank{
                ID:               id,
                Location:         Point{x, y},
                DepositOccuring:  false,
                DepositAmount:    0,
                BankOwner:        playerID,
                DepositOwner:     -1,
                DepositTicksLeft: 0,
        }
}

func (ge *GameEngine) initPads() {
        ge.EnergyPads[0] = initPad(1, 9, 8)
        ge.EnergyPads[1] = initPad(2, 10, 11)
}

func initPad(id int, x int, y int) *Pad {
        return &Pad{
                ID:        id,
                Location:  Point{x, y},
                Available: true,
                TicksLeft: 0,
        }
}

//overhead is negligible due to just 400 tiles. need to choose random tiles if the board size is increased

func (ge *GameEngine) generateBoard() {
        for x := range BOARDWIDTH {
                for y := range BOARDHEIGHT {
                        roll := rand.Float64()
                        if ((x == 6 || x == 13) && (y < 6 && y > 2 || y > 13 && y < 17)) || ((y == 6 || y == 13) && (x < 6 && x > 2 || x > 13 && x < 17)) {
                                ge.Grid[x][y].IsWall = true
                                ge.Walls = append(ge.Walls, Point{x, y})

                        } else if roll < 0.15 {
                                ge.Grid[x][y].HasAlgae = true
                                ge.AlgaeCount++
                        } else if roll < 0.20 { //5% chance of poison
                                ge.Grid[x][y].HasAlgae = true
                                ge.Grid[x][y].IsPoison = true
                        }
                }
        }
}```

```go
package engine

import (
    "math"
    "slices"
    "fmt"
)

const (
    TotalTicks        = 1000
    SpawnEnergy       = 50.0
    VisionRadius      = 4
    BaseMovementCost  = 2.0
    BaseScrapCost     = 10
    SelfDestructRange = 1
    BasePadCoolDown   = 50
    BankDepositTime   = 100
    BankDepositRange  = 4
    ScoutRadius       = 4
    BOARDWIDTH        = 20
    BOARDHEIGHT       = 20
    MAXALGAEHELD      = 5
    LockPickTime      = 20
)

const (
    PlayerOne = iota
    PlayerTwo
    Draw
)

func (engine *GameEngine) UpdateState(move PlayerMoves) {
    playerID := engine.currentPlayerID()

    for botID, spawnCmd := range move.Spawns {
                // TODO: critical, check botID <= engine.BotIDSeed[playerID] + engine.MaxBots[playerID]
        if playerID == PlayerTwo {
                        // correct?
                        spawnCmd.Location.X = 19
        }
        engine.spawnBot(spawnCmd, playerID, botID)
    }

    for botID, actionCmd := range move.Actions {
        engine.actionBot(botID, actionCmd)
    }
    engine.TickPermanentEntities()
    engine.CheckWinCondition()
    engine.Ticks++
}

func (engine *GameEngine) TickPermanentEntities() {
    for _, bank := range engine.Banks {
        if bank.LockPickOccuring {
            if bank.LockPickTicksLeft == 0 {
                bot := engine.getBot(bank.LockPickBotID)
                engine.gl.Log(GameLogDebug, fmt.Sprintf("Deposit at bankID= %d has been stolen", bank.ID))
                bank.DepositOwner = bot.OwnerID
                bank.LockPickOccuring = false
                bank.LockPickBotID = -1
            }
            if bank.LockPickTicksLeft > 0 {
                if isNearBank, _ := engine.isNearBank(bank.LockPickBotID); isNearBank{
                    bank.LockPickTicksLeft--
                } else {
                    engine.gl.Log(GameLogDebug, fmt.Sprintf("LockPick at bankID=%d has been stopped", bank.ID))
                    bank.LockPickTicksLeft = 0
                    bank.LockPickOccuring = false
                    bank.LockPickBotID = -1
                }
            }
        }
        if bank.DepositOccuring {
            if bank.DepositTicksLeft == 0 {
                engine.PermanentAlgae[bank.DepositOwner] += bank.DepositAmount
                engine.gl.Log(GameLogDebug, fmt.Sprintf("%d Deposited to Player %d at Bank %d", bank.DepositAmount, bank.DepositOwner, bank.ID))
                bank.DepositAmount = 0
                bank.DepositOccuring = false
                bank.DepositOwner = -1
            }
            if bank.DepositTicksLeft > 0 {
                bank.DepositTicksLeft--
            }
        }
    }
    for _, EnergyPad := range engine.EnergyPads {
        if EnergyPad.TicksLeft > 0 {
            if EnergyPad.TicksLeft == 1 {
                        engine.gl.Log(GameLogDebug, fmt.Sprintf("Energy Pad %d replenished", EnergyPad.ID))
            }
            EnergyPad.TicksLeft--
        }
        if EnergyPad.TicksLeft == 0 {
            EnergyPad.Available = true
        }
    }
}

func (engine *GameEngine) CheckWinCondition() int {
    if engine.PermanentAlgae[PlayerOne] > engine.AlgaeCount/2 {
        engine.gl.Log(GameLogDebug,"Player one has won")
        engine.Winner = PlayerOne
    }
    if engine.PermanentAlgae[PlayerTwo] > engine.AlgaeCount/2 {
        engine.gl.Log(GameLogDebug,"Player two has won")
        engine.Winner = PlayerTwo
    }
    if engine.Ticks >= 1000 {
        if engine.PermanentAlgae[PlayerOne] > engine.PermanentAlgae[PlayerTwo] {
            engine.gl.Log(GameLogDebug,"Player one has won")
            engine.Winner = PlayerOne
        }
        if engine.PermanentAlgae[PlayerOne] < engine.PermanentAlgae[PlayerTwo] {
            engine.gl.Log(GameLogDebug,"Player two has won")
            engine.Winner = PlayerTwo
        }
        if engine.PermanentAlgae[PlayerOne] == engine.PermanentAlgae[PlayerTwo] {
            engine.gl.Log(GameLogDebug,"Game ended in draw")
            engine.Winner = Draw
        }
    }
    return engine.Winner
}

func (engine *GameEngine) currentPlayerID() int {
    if (engine.Ticks+1) % 2 == PlayerOne {
        return PlayerOne
    } else {
        return PlayerTwo
    }
}

func (engine *GameEngine) spawnBot(spawn SpawnCmd, playerID int, botID int) bool {
    if isValid, scrapCost := engine.validateSpawn(spawn, botID); isValid {
        bot := Bot{
            ID:            botID,
            OwnerID:       playerID,
            Location:      spawn.Location,
            Energy:        SpawnEnergy,
            Scraps:        scrapCost,
            Abilities:     spawn.Abilities,
            VisionRadius:  VisionRadius,
            TraversalCost: engine.calculateTraversalCost(spawn.Abilities),
        }
        engine.AllBots[bot.ID] = &bot
        engine.Scraps[playerID] -= scrapCost
        return true
    } else {
        engine.gl.Log(GameLogWarn, fmt.Sprintf("Cannot to spawn BotID=%d", botID))
        return false
    }
}

func (engine *GameEngine) actionBot(botID int, action ActionCmd) {
    bot := engine.getBot(botID)
    if bot == nil {
        return
    }
    if validMove, energyCost := engine.validateMove(botID, action); validMove == true {
        bot.Energy -= energyCost

        if action.Direction != "NIL" {
            engine.moveBot(botID, action.Direction)
        }

        switch action.Action {
        case "HARVEST":
            engine.harvestAlgae(botID)
        case "SELFDESTRUCT":
            engine.selfDestructBot(botID)
        case "POISON":
            engine.poisonAlgae(botID)
        case "LOCKPICK":
            engine.startLockPick(botID)
        case "DEPOSIT":
            engine.startDeposit(botID)
        }
    } else {
        engine.gl.Log(GameLogWarn, fmt.Sprintf("Cannot to perform action for BotID=%d", botID))
    }
}

func incrementLocation(loc Point, direction string) (Point, bool) {
    point := loc
    switch direction {
    case "NORTH":
        point.Y++
    case "SOUTH":
        point.Y--
    case "EAST":
        point.X++
    case "WEST":
        point.X--
    }
    if point.X < 0 || point.Y < 0 || point.X > 19 || point.Y > 19 {
        return point, false
    }
    return point, true
}

func (engine *GameEngine) moveBot(botID int, direction string) {
    bot := engine.getBot(botID)
    newLocation := bot.Location
    if engine.hasAbility(botID, "SPEEDBOOST") {
        switch direction {
        case "NORTH":
            newLocation.Y += 2
        case "SOUTH":
            newLocation.Y -= 2
        case "EAST":
            newLocation.X += 2
        case "WEST":
            newLocation.X -= 2
        }

    } else {
        switch direction {
        case "NORTH":
            newLocation.Y++
        case "SOUTH":
            newLocation.Y--
        case "EAST":
            newLocation.X++
        case "WEST":
            newLocation.X--
        }
    }
    isOutOfBounds := false
    if newLocation.X < 0 {
        isOutOfBounds = true
        newLocation.X = 0
    }
    if newLocation.X > BOARDWIDTH-1 {
        isOutOfBounds = true
        newLocation.X = BOARDWIDTH-1
    }
    if newLocation.Y < 0 {
        isOutOfBounds = true
        newLocation.Y = 0
    }
    if newLocation.Y > BOARDHEIGHT-1 {
        isOutOfBounds = true
        newLocation.Y = BOARDHEIGHT-1
    }
    if isOutOfBounds {
        engine.gl.Log(GameLogWarn, "Attempted to move out of bounds", botID)
    }
    bot.Location = newLocation
    engine.energyPadCheck(botID)
}

func (engine *GameEngine) energyPadCheck(botID int) {
    bot := engine.getBot(botID)
    if OnEnergyPad, padID := engine.isOnEnergyPad(botID); OnEnergyPad {
        pad := engine.EnergyPads[padID]
        if pad.Available {
            pad.Available = false
            pad.TicksLeft = engine.getPadCoolDown()
            bot.Energy = float64(SpawnEnergy)
        }
    }
}

func (engine *GameEngine) getPadCoolDown() int {
    if engine.Ticks < TotalTicks*3/10 {
        return BasePadCoolDown
    }
    if engine.Ticks < TotalTicks*5/10 {
        return BasePadCoolDown * 5 / 10
    }
    if engine.Ticks < TotalTicks*7/10 {
        return BasePadCoolDown * 1 / 4
    }
    return BasePadCoolDown * 2 / 10
}

func (engine *GameEngine) selfDestructBot(botID int) {
    bot := engine.getBot(botID)
    for _, botB := range engine.AllBots {
        if math.Abs(float64(bot.Location.X-botB.Location.X)) <= SelfDestructRange && math.Abs(float64(bot.Location.Y-botB.Location.Y)) <= SelfDestructRange {
            if engine.hasAbility(botB.ID, "SHIELD") {
                engine.removeShield(botB.ID)
            } else {
                engine.KillBot(botB.ID)
            }
        }
    }
    engine.KillBot(bot.ID)
}

func (engine *GameEngine) KillBot(botID int) {
    delete(engine.AllBots, botID)
}

func (engine *GameEngine) removeShield(botID int) {
    bot := engine.getBot(botID)
    newAbilities := make([]string, 0, len(bot.Abilities)-1)
    for _, ability := range bot.Abilities {
        if ability != "SHIELD" {
            newAbilities = append(newAbilities, ability)
        }
    }
    bot.TraversalCost -= EnergyDB["SHIELD"].Traversal
    bot.Abilities = newAbilities
}

func (engine *GameEngine) validateSpawn(spawn SpawnCmd, botID int) (bool, int) {
    scrapCost := 0
    playerID := engine.currentPlayerID()
    bot := engine.getBot(botID)
    if bot != nil {
        engine.gl.Log(GameLogWarn, fmt.Sprintf("BotID=%d already exists", botID))
        return false, scrapCost
    }

    if engine.LocationOccupied(spawn.Location) {
        engine.gl.Log(GameLogWarn, fmt.Sprintf("BotID=%d attempted spawn at occupied location", botID))
        return false, scrapCost
    }

    for _, ability := range spawn.Abilities {
        scrapCost += CostDB[ability]
    }

    if scrapCost > engine.Scraps[playerID] {
        engine.gl.Log(GameLogWarn, fmt.Sprintf("BotID=%d does not have enough scraps to spawn", botID))
        return false, scrapCost
    }
    return true, scrapCost

}

func (engine *GameEngine) LocationOccupied(point Point) bool {
    // TODO: What about other factors like banks ?
    for _, bot := range engine.AllBots {
        if point == bot.Location {
            return true
        }
    }
    return false
}

func (engine *GameEngine) validateMove(botID int, move ActionCmd) (bool, float64) {
    playerID := engine.currentPlayerID()
    bot := engine.getBot(botID)
    energyCost := 0.0
    if bot == nil {
        engine.gl.Log(GameLogWarn, fmt.Sprintf("Invalid BotID %d", botID))
        return false, energyCost
    }
    if bot.OwnerID != playerID {
        engine.gl.Log(GameLogWarn, fmt.Sprintf("Player %d attempted to control invalid Bot %d", playerID, botID))
        return false, energyCost
    }

    if move.Direction != "NULL" {
        point, ok := incrementLocation(bot.Location, move.Direction)
        if !ok {
            engine.gl.Log(GameLogWarn, fmt.Sprintf("botID=%d attempted to move out of bounds at (%d %d)", botID, point.X, point.Y))
            return false, energyCost
        }
        if engine.LocationOccupied(point) {
            engine.gl.Log(GameLogWarn, fmt.Sprintf("botID=%d attempted to move at Occupied Location at (%d %d)", botID, point.X, point.Y))
            return false, energyCost
        }
        if engine.isWall(point){
            engine.gl.Log(GameLogWarn, fmt.Sprintf("botID=%d attempted to move to a wall at (%d %d)", botID, point.X, point.Y))
            return false, energyCost
        }
        energyCost += bot.TraversalCost
    }
    if move.Action != "MOVE"{
        if !engine.hasAbility(botID, move.Action) {
            engine.gl.Log(GameLogWarn, fmt.Sprintf("botID=%d does not have ability=%s", botID, move.Action))
            return false, energyCost
        }
    }

    energyCost += EnergyDB[move.Action].Ability

    if energyCost > bot.Energy {
        engine.gl.Log(GameLogWarn, fmt.Sprintf("botID=%d does not have enough energy for ability=%s", botID, move.Action))
        return false, energyCost
    }

    return true, energyCost
}
```