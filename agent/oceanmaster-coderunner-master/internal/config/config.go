package config

import (
	"os"
	"strconv"
)

type QueuesConfig struct {
	URL               string
	RankedQueueName   string
	PracticeQueueName string
}

type S3Config struct {
	FileURL         string
	AccessKeyID     string
	SecretAccessKey string
	Region          string
	Bucket          string
	Endpoint        string
}

type Config struct {
	ApiURL   string
	ApiToken string

	IsProd               bool
	MaxConcurrentMatches int

	QueuesConfig QueuesConfig

	NsjailPath    string
	NsjailCfgPath string

	WrapperPyPath      string
	HostSubmissionPath string

	JailHostname          string
	JailCwd               string
	JailSubmissionPath    string
	JailCGroupPidsMax     uint64
	JailCGroupMemMax      uint64
	JailCGroupCpuMsPerSec uint32
	JailTmpfsSize         uint64

	JailWallTimeoutMS      uint32
	JailHandshakeTimeoutMS uint32
	JailTickTimeoutMS      uint32

	S3Config S3Config
}

func New() *Config {
	isProd := os.Getenv("PROD") == "true"

	return &Config{
		ApiURL:   getEnv("API_URL", "http://manager:8080"),
		ApiToken: getEnv("API_TOKEN", ""),

		IsProd:               isProd,
		MaxConcurrentMatches: getEnv("MAX_CONCURRENT_MATCHES", 10),

		QueuesConfig: QueuesConfig{
			URL:               getEnv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672"),
			RankedQueueName:   getEnv("RABBITMQ_RANKED_QUEUE", "match.queue"),
			PracticeQueueName: getEnv("RABBITMQ_PRACTICE_QUEUE", "practice.queue"),
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

		S3Config: S3Config{
			FileURL:         getEnv("S3_FILE_URL", ""),
			AccessKeyID:     getEnv("S3_ACCESS_KEY_ID", ""),
			SecretAccessKey: getEnv("S3_SECRET_ACCESS_KEY", ""),
			Region:          getEnv("S3_REGION", ""),
			Bucket:          getEnv("S3_BUCKET", ""),
			Endpoint:        getEnv("S3_ENDPOINT", ""),
		},
	}
}

func getEnv[T string | int](k string, d T) T {
	v := os.Getenv(k)
	if v == "" {
		return d
	}

	var result T

	switch any(d).(type) {
	case string:
		result = any(v).(T)
	case int:
		i, err := strconv.Atoi(v)
		if err != nil {
			panic(err)
		}
		result = any(i).(T)
	default:
		panic("unsupported type")
	}

	return result
}
