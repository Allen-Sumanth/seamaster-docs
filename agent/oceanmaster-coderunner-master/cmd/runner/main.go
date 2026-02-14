package main

import (
	"context"
	"encoding/json"
	"log"
	"os"
	"os/signal"
	"sync"
	"syscall"

	"github.com/delta/code-runner/internal/cgroup"
	"github.com/delta/code-runner/internal/config"
	"github.com/delta/code-runner/internal/manager"
	"github.com/delta/code-runner/internal/nsjail"
	"github.com/delta/code-runner/internal/queue"
	storage "github.com/delta/code-runner/internal/s3"
	"github.com/rabbitmq/amqp091-go"
)

func run() error {
	cfg := config.New()

	cg, err := cgroup.UnshareAndMount()
	if err != nil {
		return err
	}

	_, err = nsjail.WriteConfig(cfg, cg)
	if err != nil {
		return err
	}

	s3Client, err := storage.NewS3Client(cfg.S3Config)
	if err != nil {
		return err
	}

	gameManager := manager.NewGameManager(cfg, s3Client)

	matchJobQ, err := queue.NewQueuesConsumer(cfg.QueuesConfig, cfg.MaxConcurrentMatches)
	if err != nil {
		return err
	}
	defer matchJobQ.Close()

	msgs, err := matchJobQ.Consume()
	if err != nil {
		return err
	}

	sem := make(chan struct{}, cfg.MaxConcurrentMatches)
	var wg sync.WaitGroup

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, os.Interrupt, syscall.SIGTERM)

	go func() {
		<-sigChan
		log.Println("Shutdown signal received, waiting for matches to complete...")
		cancel()
	}()

	log.Printf("consumer started with %d max_concurrency\n", cfg.MaxConcurrentMatches)

	for {
		select {
		case <-ctx.Done():
			log.Println("Waiting for active matches to finish...")
			wg.Wait()
			log.Println("All matches completed, shutting down")
			return nil

		case d, ok := <-msgs:
			if !ok {
				log.Println("Message channel closed, initiating shutdown...")
				cancel()
				continue
			}

			sem <- struct{}{} // blocks if max concurrency reached
			wg.Add(1)

			go func(delivery amqp091.Delivery) {
				defer func() {
					if r := recover(); r != nil {
						log.Printf("PANIC in match processing: %v", r)
						delivery.Nack(false, true) // requeue on panic
					}
					<-sem
					wg.Done()
				}()

				var job manager.MatchJob
				if err := json.Unmarshal(delivery.Body, &job); err != nil {
					log.Println("INVALID JOB:", err)
					delivery.Nack(false, false) // discard
					return
				}

				log.Println("RUNNING MATCH:", job.ID)

				if err := gameManager.NewMatch(job); err != nil {
					log.Println("MATCH FAILED:", err)
					delivery.Nack(false, false)
					// TODO: Implement retry count tracking and dead-letter after N attempts
					return
				}

				log.Println("MATCH FINISHED:", job.ID)
				delivery.Ack(false)
			}(d)
		}
	}
}

func main() {
	if err := run(); err != nil {
		log.Fatal(err)
	}
}