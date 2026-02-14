package queue

import (
	"errors"
	"log"

	"github.com/delta/code-runner/internal/config"
	"github.com/rabbitmq/amqp091-go"
)

type QueuesConsumer struct {
	cfg          config.QueuesConfig
	conn         *amqp091.Connection
	ch           *amqp091.Channel
	outStreamLen int
}

func (q *QueuesConsumer) Consume() (<-chan amqp091.Delivery, error) {
	rankedMsgs, err := q.ch.Consume(
		q.cfg.RankedQueueName,
		"",
		false,
		false,
		false,
		false,
		nil,
	)
	if err != nil {
		return nil, err
	}

	practiceMsgs, err := q.ch.Consume(
		q.cfg.PracticeQueueName,
		"",
		false,
		false,
		false,
		false,
		nil,
	)
	if err != nil {
		return nil, err
	}

	out := make(chan amqp091.Delivery, q.outStreamLen+5)
	closeNotify := q.conn.NotifyClose(make(chan *amqp091.Error, 1))

	go func() {
		defer close(out)
		for rankedMsgs != nil || practiceMsgs != nil {
			select {
			case <-closeNotify:
				log.Println("RabbitMQ connection closed")
				return

			case d, ok := <-rankedMsgs:
				if !ok {
					rankedMsgs = nil
					continue
				}
				out <- d

			case d, ok := <-practiceMsgs:
				if !ok {
					practiceMsgs = nil
					continue
				}
				out <- d
			}
		}
	}()

	return out, nil
}

func NewQueuesConsumer(cfg config.QueuesConfig, maxConcurrentMatches int) (*QueuesConsumer, error) {
	conn, err := amqp091.Dial(cfg.URL)
	if err != nil {
		return nil, err
	}

	ch, err := conn.Channel()
	if err != nil {
		conn.Close()
		return nil, err
	}

	_, err = ch.QueueDeclare(
		cfg.RankedQueueName,
		true,
		false,
		false,
		false,
		nil,
	)
	if err != nil {
		ch.Close()
		conn.Close()
		return nil, err
	}

	_, err = ch.QueueDeclare(
		cfg.PracticeQueueName,
		true,
		false,
		false,
		false,
		nil,
	)
	if err != nil {
		ch.Close()
		conn.Close()
		return nil, err
	}

	// Set prefetch count to match max concurrent matches for optimal throughput
	err = ch.Qos(maxConcurrentMatches, 0, false)
	if err != nil {
		ch.Close()
		conn.Close()
		return nil, err
	}

	return &QueuesConsumer{
		cfg:          cfg,
		conn:         conn,
		ch:           ch,
		outStreamLen: maxConcurrentMatches,
	}, nil
}

func (q *QueuesConsumer) Close() error {
	var chErr, connErr error

	if q.ch != nil {
		chErr = q.ch.Close()
	}

	if q.conn != nil {
		connErr = q.conn.Close()
	}

	if chErr != nil {
		return chErr
	}
	if connErr != nil {
		return connErr
	}

	if q.ch == nil && q.conn == nil {
		return errors.New("already closed")
	}

	return nil
}