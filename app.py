import os
from flask import Flask
from flask import flash, g, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy

# Configuration lines
app = Flask(__name__)
db_path = os.path.join(os.path.dirname(__file__), 'database.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = 'dev'
db = SQLAlchemy(app)


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



