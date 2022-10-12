package main

import (
	"flag"
	"log"
)

func main() {
	flag.Parse()
	args := flag.Args()
	if len(args) != 1 {
		log.Panicln("error. do `go run {THIS_FILE} {COMMIT_REVISION}`")
	}

}
