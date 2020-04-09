import os
import pandas as pd
from flask import Flask, jsonify, request
from flask_restplus import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

# Configuration lines
app = Flask(__name__)
api = Api(app, version='1.1', title='Vertias Wrestling System API',
    description='API for VWS freestyle wresting data.'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE')
db = SQLAlchemy(app)
tables_dict = {
    'wrestler': 'vws_main_fs_wrestler',
    'team': 'vws_main_fs_team',
    'match': 'vws_main_fs_match',
    'timeseries': 'vws_main_fs_ts',
}

# Reflects tables for GET requests only!
wrestlers = db.Table(tables_dict['wrestler'], db.metadata, autoload=True, autoload_with=db.engine)
teams = db.Table(tables_dict['team'], db.metadata, autoload=True, autoload_with=db.engine)
matches = db.Table(tables_dict['match'], db.metadata, autoload=True, autoload_with=db.engine)
timeseries = db.Table(tables_dict['timeseries'], db.metadata, autoload=True, autoload_with=db.engine)

### API SECTION
#Get info for one team
@api.route('/v1/team/<string:teamname_slug>/info')
class TeamInfo(Resource):
    def get(self, teamname_slug):
        q = db.session.query(teams).filter_by(name=func.upper(teamname_slug)
            ).first_or_404(description=f"There is no team data for slug: {teamname_slug}")
        return jsonify(name=q.name) 

#Get info for one wrestler
@api.route('/v1/wrestler/<string:name_slug>/info')
class WrestlerInfo(Resource):
    def get(self, name_slug):
        q = db.session.query(wrestlers).filter_by(slug=name_slug
            ).first_or_404(description=f"There is no athlete data for slug: {name_slug}")
        return jsonify(name=q.name, team=q.team_id, rating=q.rating, slug=q.slug) 

# Get average stats for a single wrestler
@api.route('/v1/wrestler/<string:name_slug>/stats')
class WrestlerStats(Resource):
    def get(self, name_slug):
        name = ' '.join(n for n in name_slug.split('-'))
        q = db.session.query(
            func.avg(matches.c.vs), 
            func.avg(matches.c.npf), 
            func.avg(matches.c.focus_score),
            func.avg(matches.c.opp_score),
            ).group_by(matches.c.focus_id).filter(
                func.lower(matches.c.focus_id) == name
                    ).first_or_404(description=f"There is no team data for slug: {name_slug}")
                    
        return jsonify(
            avg_vs=float(q[0]), 
            avg_npf=float(q[1]),
            avg_points=float(q[2]),
            avg_opp_points=float(q[3]),
        ) 

