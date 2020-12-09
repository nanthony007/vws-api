package controllers

import (
	"fmt"
	"github.com/nanthony007/vws-api/api/models"
	"log"
	"net/http"

	"github.com/jmoiron/sqlx"
	"github.com/joho/godotenv"
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
	_ "github.com/lib/pq"
)

// Server contains the database and router.
type Server struct {
	DB     *sqlx.DB
	Router *echo.Echo
}

// Initialize connects to the database and creates the router using the Server struct.
// Requires database credentials to be passed, assumes postgresql database.
func (server *Server) Initialize(DbUser, DbPassword, DbPort, DbHost, DbName string) {

	var err error

	DBURL := fmt.Sprintf("host=%s port=%s user=%s dbname=%s sslmode=require password=%s", DbHost, DbPort, DbUser, DbName, DbPassword)
	server.DB, err = sqlx.Connect("postgres", DBURL)
	if err != nil {
		fmt.Printf("Cannot connect to database")
		log.Fatal("This is the error:", err)
	} else {
		fmt.Printf("We are connected to the database")
	}

	server.Router = echo.New()
	server.Router.Use(middleware.LoggerWithConfig(middleware.LoggerConfig{
		Format: "method=${method}, uri=${uri}, status=${status}\n",
	}))

	server.initializeRoutes()
}

// Run starts the server on port 8080.
func (server *Server) Run(addr string) {
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}
	fmt.Println("Listening to port 8080")
	log.Fatal(server.Router.Start(addr))
}

// Home returns a JSON welcome message on the server.
func (s *Server) Home(c echo.Context) error {
	return c.JSON(http.StatusOK, "Welcome To This Awesome API")
}

// GetWrestlers queries the db and returns json results.
func (s *Server) GetWrestlers(c echo.Context) error {

	limit := c.QueryParam("limit")
	if limit == "" {
		limit = "10"
	} else if limit == "-1" {
		limit = ""
	}

	wrestler := models.WrestlerInfo{}

	wrestlers, err := wrestler.FindWrestlers(s.DB, limit)
	if err != nil {
		fmt.Println(err)
		return c.JSON(http.StatusInternalServerError, wrestler)
	}
	return c.JSON(http.StatusOK, wrestlers)
}
