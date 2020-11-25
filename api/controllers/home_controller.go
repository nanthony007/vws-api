package controllers

import (
	"net/http"

	"github.com/labstack/echo/v4"
)

// Home returns a JSON welcome message on the server.
func (s *Server) Home(c echo.Context) error {
	return c.JSON(http.StatusOK, "Welcome To This Awesome API")
}
