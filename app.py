"""Blogly application."""

from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

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
    users = User.query.order_by(User.last_name, User.first_name).all()
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
    
    return redirect(f'/users/{new_user.id}')

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

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_user(user_id):
    """Update user in database and redirect to users detail page."""
    user = User.query.get_or_404(user_id)
    
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form['image-url'] or None
    
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.add(user)
    db.session.commit()
    
    return redirect(f'/users/{user.id}')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete user from database."""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    
    return redirect('/')
    
@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    """Show form to add a new post."""
    user = User.query.get_or_404(user_id)
    return render_template('new_post_form.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def handle_adding_new_post(user_id):
    """Handle add form; add post and redirect to the user detail page."""
    user = User.query.get_or_404(user_id)
    
    title = request.form['title']
    content = request.form['content']
    
    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    
    return redirect(f'/users/{user.id}')