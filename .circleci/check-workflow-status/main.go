package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/joho/godotenv"
)

type listOfPipelines struct {
	Items []struct {
		ID     string `json:"id"`
		Errors []struct {
			Type    string `json:"type"`
			Message string `json:"message"`
		} `json:"errors"`
		ProjectSlug       string    `json:"project_slug"`
		UpdatedAt         time.Time `json:"updated_at"`
		Number            int       `json:"number"`
		TriggerParameters struct {
			Property1 string `json:"property1"`
			Property2 string `json:"property2"`
		} `json:"trigger_parameters"`
		State     string    `json:"state"`
		CreatedAt time.Time `json:"created_at"`
		Trigger   struct {
			Type       string    `json:"type"`
			ReceivedAt time.Time `json:"received_at"`
			Actor      struct {
				Login     string `json:"login"`
				AvatarURL string `json:"avatar_url"`
			} `json:"actor"`
		} `json:"trigger"`
		Vcs struct {
			ProviderName        string `json:"provider_name"`
			TargetRepositoryURL string `json:"target_repository_url"`
			Branch              string `json:"branch"`
			ReviewID            string `json:"review_id"`
			ReviewURL           string `json:"review_url"`
			Revision            string `json:"revision"`
			Tag                 string `json:"tag"`
			Commit              struct {
				Subject string `json:"subject"`
				Body    string `json:"body"`
			} `json:"commit"`
			OriginRepositoryURL string `json:"origin_repository_url"`
		} `json:"vcs"`
	} `json:"items"`
	NextPageToken string `json:"next_page_token"`
}

type request_option struct {
	org_slug     string
	circle_token string
	revision     string
}

func get_pipeline_id_list(o request_option) ([]string, error) {
	url := fmt.Sprintf("https://circleci.com/api/v2/pipeline?org-slug=%s&mine=true", o.org_slug)
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		return nil, err
	}

	req.Header.Set("Circle-Token", o.circle_token)
	client := new(http.Client)
	resp, err := client.Do(req)
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	var listOfPipelines listOfPipelines
	if err := json.Unmarshal(body, &listOfPipelines); err != nil {
		return nil, err
	}

	log.Println(listOfPipelines)

	return []string{}, nil
}

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

	org_slug := os.Getenv("ORG_SLUG")
	circle_token := os.Getenv("CIRCLE_TOKEN")
	ro := request_option{
		org_slug:     org_slug,
		circle_token: circle_token,
	}

	_, err = get_pipeline_id_list(ro)
	if err != nil {
		log.Panicln(err)
	}
}
