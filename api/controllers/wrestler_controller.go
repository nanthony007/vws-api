package controllers

import (
	"fmt"
	"net/http"

	"github.com/labstack/echo/v4"
	"github.com/nanthony007/vws-api/api/models"
)

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
