"""Blogly application."""

from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

#Users routes
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

#Posts routes
@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show details for single post."""
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    """Show form to edit post."""
    post = Post.query.get_or_404(post_id)
    return render_template('edit_post.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def update_post(post_id):
    """Show form to edit post."""
    post = Post.query.get_or_404(post_id)
    
    post.title = request.form['title']
    post.content = request.form['content']
    
    db.session.add(post)
    db.session.commit()
    
    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete',  methods=['POST'])
def delete_post(post_id):
    """Delete a post."""
    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    
    db.session.delete(post)
    db.session.commit()
    
    return redirect(f'/users/{user_id}')

#Tags routes
@app.route('/tags')
def list_tags():
    """Lists all tags, with links to the tag detail page."""
    tags = Tag.query.all()
    
    return render_template('all_tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag_detail(tag_id):
    """Show detail about a tag. Have links to edit form and to delete."""
    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts
    
    return render_template('show_tag.html', tag=tag, posts=posts)

@app.route('/tags/new')
def  new_tag_form():
    """Form to create a new tag."""
    return render_template('new_tag_form.html')

@app.route('/tags/new', methods=['POST'])
def  create_new_tag():
    """Add new tag to database."""
    name = request.form['name']
    
    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()
    
    return redirect(f'/tags/{new_tag.id}')

@app.route('/tags/<int:tag_id>/edit')
def edit_tag_form(tag_id):
    """Form to edit tag"""
    tag = Tag.query.get_or_404(tag_id)
    
    return render_template('edit_tag_form.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tag_form(tag_id):
    """Form to edit tag"""
    tag = Tag.query.get_or_404(tag_id)
    
    tag.name = request.form['name']
    
    db.session.add(tag)
    db.session.commit()
    
    return redirect(f'/tags/{tag.id}')