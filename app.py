import os
import pandas as pd
from flask import Flask, jsonify, flash, g, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api

# Configuration lines
app = Flask(__name__)
db_path = os.path.join(os.path.dirname(__file__), 'database.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = 'dev'
db = SQLAlchemy(app)  # connects database
api = Api(app)  # configures api
df = pd.read_csv('VWS.csv')

### MODELS SECTION
# User table with fields
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


### ROUTES SECTION
# Home page route, renders home.html template
@app.route('/', methods=('POST', 'GET'))
def home():
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first() # Searches for user

        # If user, clear session and set as active user
        if user is not None:
            session.clear()
            session['user_id'] = user.id
            flash('Login succesful.', 'success') # Flash message to frontend
            return redirect(url_for('home'))

        # If not valid user, flash message to frontend to try again
        elif user is None:
            flash('Invalid username. Please try again.', 'danger')
            return render_template('home.html')

    # Get user info if exists and save in global 'g' variable
    elif request.method == 'GET':
        user_id = session.get('user_id')
        if user_id is None:
            g.user = None
        else:
            g.user = User.query.filter_by(id=user_id).first()
        return render_template('home.html')

@app.route('/about')
def about():
    # Get user info if exists and save in global 'g' variable
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first()
    return render_template('about.html')

@app.route('/usage')
def usage():
    # Get user info if exists and save in global 'g' variable
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first()
    return render_template('usage.html')

@app.route('/contact')
def contact():
    # Get user info if exists and save in global 'g' variable
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first()
    return render_template('contact.html')

@app.route('/logout')
def logout():
    # Clears session of user info for logout and flashes message to frontend
    session.clear()
    flash('Logout successful', 'success')
    return render_template('logout.html')


### API SECTION
# Get list of teams
class TeamList(Resource):
    def get(self):
        df_teams = sorted(df.Team1.unique())
        return {i:x for i,x in enumerate(df_teams)}

# Get list of wrestlers
class WrestlerList(Resource):
    def get(self):
        df_wrestlers = sorted(df.WID.unique())
        return {i:x for i,x in enumerate(df_wrestlers)}

# Get stats for a wrestler
class WrestlerStats(Resource):
    def get(self, wid):
        wid_changed = wid.replace('-', ' ').title()
        df_wrestler_stats = df.groupby('WID').mean().loc[wid_changed]
        return dict(zip(df_wrestler_stats.keys(), df_wrestler_stats.values.round(2)))

# Add resources to api
api.add_resource(TeamList, '/api/v1/teams')
api.add_resource(WrestlerList, '/api/v1/wrestlers')
api.add_resource(WrestlerStats, '/api/v1/wrestlerstats/<string:wid>')
