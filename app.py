"""Blogly application."""

from email.mime import image
from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

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

@app.route('/users/new')
def show_new_user_form():
    """Render form to create new user."""
    return render_template('new_user_form.html')

@app.route('/users/new', methods=['POST'])
def create_user():
    """Post route to create new user and add to database."""
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form['image-url'] or None
    
    new_user = User(first_name = first_name, last_name = last_name, image_url = image_url)
    db.session.add(new_user)
    db.session.commit()
    
    return redirect(f'/{new_user.id}')

@app.route('/users/<int:user_id>')
def show_user_detail(user_id):
    """Show details about a single user."""
    user = User.query.get_or_404(user_id)
    return render_template('user_detail.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user_detail(user_id):
    """Edit details about a single user."""
    user = User.query.get_or_404(user_id)
    return render_template('edit_user_form.html', user=user)