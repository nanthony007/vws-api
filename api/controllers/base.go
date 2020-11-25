package controllers

import (
	"fmt"
	"log"

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
