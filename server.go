package main

import (
	"log"
	"math"
	"net/http"
	"os"
	"strings"

	"github.com/jmoiron/sqlx"
	"github.com/joho/godotenv"

	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"

	_ "github.com/lib/pq"
)

// use godot package to load/read the .env file and
// return the value of the key
func goDotEnvVariable(key string) string {

	// load .env file
	err := godotenv.Load(".env")

	if err != nil {
		log.Fatalf("Error loading .env file")
	}

	return os.Getenv(key)
}

// Wrestler container to hold name, rating, and team.
type Wrestler struct {
	Name   string `db:"name"`
	Rating int    `db:"rating"`
	Team   string `db:"team_id"`
}

// WrestlerStats container to hold name and average of statistics.
type WrestlerStats struct {
	Name              string  `db:"focus_id"`
	VeritasScore      float64 `db:"vs"`
	NeutralPaceFactor float64 `db:"npf"`
	Points            float64 `db:"focus_score"`
	OppPoints         float64 `db:"opp_score"`
}

// Team container to hold general info.
type Team struct {
	Abbreviation string `db:"abbreviation"`
	Name         string `db:"name"`
	Slug         string `db:"slug"`
}

func sum(array []float64) float64 {
	result := 0.0
	for _, v := range array {
		result += v
	}
	return result
}

func main() {
	port := os.Getenv("PORT")

	if port == "" {
		log.Fatal("$PORT must be set")
	}

	var db *sqlx.DB

	db, err := sqlx.Connect("postgres", "postgres://ibpfcwfnmikxmw:5f6f81e84894399cc02a1ad09a6a663d21d448e9b4cbe2897d5fc75817818d3a@ec2-54-83-9-36.compute-1.amazonaws.com:5432/dfh945lu8avc08")

	if err != nil {
		log.Fatalln(err)
	}

	e := echo.New()
	e.Use(middleware.LoggerWithConfig(middleware.LoggerConfig{
		Format: "method=${method}, uri=${uri}, status=${status}\n",
	}))

	e.GET("/", func(c echo.Context) error {
		return c.JSON(http.StatusOK, "Welcome")
	})
	e.GET("/wrestlers", func(c echo.Context) error {
		wrestlers := []Wrestler{}
		var limit string
		limit = c.QueryParam("top")

		if limit == "" {
			db.Select(&wrestlers, "SELECT name, rating, team_id FROM vws_main_fs_wrestler ORDER BY rating DESC")
			return c.JSON(http.StatusOK, wrestlers)
		}
		db.Select(&wrestlers, "SELECT name, rating, team_id FROM vws_main_fs_wrestler ORDER BY rating DESC LIMIT $1;", limit)
		return c.JSON(http.StatusOK, wrestlers)

	})
	e.GET("/wrestlers/stats/:name", func(c echo.Context) error {
		name := c.Param("name")
		formattedName := strings.Replace(name, "-", " ", 1)
		stats := []WrestlerStats{}
		db.Select(&stats, "SELECT focus_id, focus_score, opp_score, npf, vs FROM vws_main_fs_match WHERE focus_id ILIKE $1", formattedName)

		var vs, npf, pts, opts []float64
		for i := range stats {
			vs = append(vs, stats[i].VeritasScore)
			npf = append(npf, stats[i].NeutralPaceFactor)
			pts = append(pts, stats[i].Points)
			opts = append(opts, stats[i].OppPoints)
		}
		wrestler := new(WrestlerStats)
		wrestler.Name = stats[0].Name
		wrestler.VeritasScore = math.Round(sum(vs)*100) / 100
		wrestler.NeutralPaceFactor = math.Round(sum(npf)*100) / 100
		wrestler.Points = math.Round(sum(pts)*100) / 100
		wrestler.OppPoints = math.Round(sum(opts)*100) / 100
		return c.JSON(http.StatusOK, wrestler)
	})

	e.Logger.Fatal(e.Start(":" + port))
}
