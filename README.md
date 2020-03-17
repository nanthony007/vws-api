# RESTful API for Veritas Wrestling Systems
## This project is to create a simple website with an API component for wrestler statistics and is under active development, check back frequently for updates.
---
To install project use `git clone` then `cd wrestlerAPI`.

Then create a conda environment using the *environment.yml* file:
`conda env create -f environment.yml`. 

Then `conda activate wres-api`.

All variables *should* be configured in the source code.

On Mac/Linux:
`export FLASK_APP=app.py` & 
`export FLASK_ENV=development`.

On Windows:
`set FLASK_APP=app.py` & 
`set FLASK_ENV=development`.

Then a simple `flask run` and view `localhost:5000`.

---
### API Documentation
Main url: https://folkstyle-wrestler-api.herokuapp.com/api/v1

GET list of wrestlers: '/wrestlers'

GET list of teams: '/teams'

GET stats for one wrestler: 'wrestlerstats/<wid:string>'
Translate WID into url-compliant version (Anthony Florida 141 becomes anthony-florida-141)

---

> Task list here!
