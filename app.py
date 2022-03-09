"""Blogly application."""

from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def index():
    """Redirect to page listing all users."""
    return redirect('/users')

@app.route('/users')
def show_users():
    """Page showing all users."""
    users = User.query.all()
    return render_template('users.html', users=users)