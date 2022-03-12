"""Models for Blogly."""
from unicodedata import name
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)
    
class User(db.Model):
    """Users model"""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    first_name = db.Column(db.String(50), nullable = False)
    last_name = db.Column(db.String(50), nullable = False)
    image_url = db.Column(db.Text, nullable = False, 
                        default = "https://images.unsplash.com/photo-1533738363-b7f9aef128ce?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=735&q=80")
    
    posts = db.relationship("Post", backref="users", cascade="all, delete-orphan")
    
    def __repr__(self):
        """Representation of User Instance"""
        u = self
        return f"<User id={u.id} first_name={u.first_name} last_name={u.last_name} image_url={u.image_url}>"
    
    @property
    def full_name(self):
        """Show first and last names concatenated together."""
        return f"{self.first_name} {self.last_name}"
    
class Post(db.Model):
    """Posts model"""
    
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String(40), nullable = False)
    content = db.Column(db.Text, nullable = False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="cascade"), nullable=False)
    
    #Relationship to PostTag
    posts_tags = db.relationship("PostTag", backref="posts", cascade="all, delete-orphan")
    
    #Through relationship to Tag
    tags = db.relationship("Tag", secondary="posts_tags", backref="posts")
    
    def __repr__(self):
        """Representation of Post Instance"""
        p = self
        return f"<Post id={p.id} title={p.title} created_at={p.created_at} user_id={p.user_id}>"
    
class Tag(db.Model):
    """Tags model"""
    
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(30), nullable = False, unique=True)
    
    #Relationship to PostTag
    posts_tags = db.relationship("PostTag", backref="tags", cascade="all, delete-orphan")
    
    def __repr__(self):
        """Representation of Tag Instance"""
        t = self
        return f"<Tag id={t.id} name={t.name}>"
    
class PostTag(db.Model):
    """Mapping of a posts to tags."""
    
    __tablename__ = 'posts_tags'
    
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id", ondelete="cascade"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id", ondelete="cascade"), primary_key=True)
    
    def __repr__(self):
        """Representation of PostTag Instance"""
        pt = self
        return f"<PostTag post_id={pt.post_id} tag_id={pt.tag_id}>"