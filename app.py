import os
from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

# Configuration lines
app = Flask(__name__)
db_path = os.path.join(os.path.dirname(__file__), 'database.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

# User table with fields
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

# Home page route, renders home.html template
@app.route('/')
def home():
    return render_template('home.html')

