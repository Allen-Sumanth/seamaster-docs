package manager

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"time"

	"github.com/delta/code-runner/internal/config"
	"github.com/delta/code-runner/internal/engine"
	"github.com/google/uuid"
	"github.com/minio/minio-go/v7"
)

func PostResults(s3Client *minio.Client, cfg *config.Config, matchID int, results *engine.MatchResults, path string) error {
	results.MatchID = matchID

	key := fmt.Sprintf("matches/%s.txt", uuid.NewString())

	start := time.Now()

	_, err := s3Client.FPutObject(
		context.Background(),
		cfg.S3Config.Bucket,
		key,
		path,
		minio.PutObjectOptions{
			ContentType: "text/plain",
		},
	)
	if err != nil {
		return err
	}

	fmt.Printf("Uploaded %d results to S3 in %s\n", matchID, time.Since(start))

	results.LogURL = fmt.Sprintf("%s/%s", cfg.S3Config.FileURL, key)

	body, err := json.Marshal(results)
	if err != nil {
		return err
	}

	fmt.Println(matchID, results)

	req, err := http.NewRequest("POST", cfg.ApiURL+"/results", bytes.NewBuffer(body))
	if err != nil {
		return err
	}

	req.Header.Set("Authorization", "Bearer "+cfg.ApiToken)
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{
		Timeout: 15 * time.Second,
	}

	resp, err := client.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	if resp.StatusCode < 200 || resp.StatusCode >= 300 {
		return fmt.Errorf("results POST failed: %s", resp.Status)
	}

	return nil
}
