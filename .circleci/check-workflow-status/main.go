package main

import (
	"flag"
	"log"
	"os"

	"github.com/joho/godotenv"
)

func main() {
	flag.Parse()
	args := flag.Args()
	if len(args) != 1 {
		log.Panicln("error. do `go run {THIS_FILE} {COMMIT_REVISION}`")
	}

	err := godotenv.Load()
	if err != nil {
		log.Panicln("Error loading .env file")
	}

	_ = os.Getenv("ORG_SLUG")
	_ = os.Getenv("CIRCLE_TOKEN")
}
