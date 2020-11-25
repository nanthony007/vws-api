package models

import (
	"github.com/jmoiron/sqlx"
)

// WrestlerInfo implements a model with basic wrestler information.
type WrestlerInfo struct {
	Name   string `db:"name" json:"name"`
	Rating int    `db:"rating" json:"rating"`
	Team   string `db:"team_id" json:"team"`
}

// FindWrestlers queries the database for `n` wrestler's information.
func (u *WrestlerInfo) FindWrestlers(db *sqlx.DB, n string) (*[]WrestlerInfo, error) {
	var query string
	if n == "" {
		query = `
			SELECT name, rating, team_id 
			FROM vws_main_fs_wrestler
		`
	} else {
		query = `
			SELECT name, rating, team_id 
			FROM vws_main_fs_wrestler
			ORDER BY name
			LIMIT 
		` + n
	}
	var err error
	wrestlers := []WrestlerInfo{}
	err = db.Select(&wrestlers, query)
	if err != nil {
		return &[]WrestlerInfo{}, err
	}
	return &wrestlers, err
}
