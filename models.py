"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)
    
class User(db.Model):
    """Users Model"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    
    first_name = db.Column(db.String(50), nullable = False)
    
    last_name = db.Column(db.String(50), nullable = False)
    
    image_url = db.Column(db.Text, nullable = False, default = "https://images.unsplash.com/photo-1533738363-b7f9aef128ce?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=735&q=80")
    
    def __repr__(self):
        """Representation of User Instance"""
        u = self
        return f"<User id={u.id} first_name={u.first_name} last_name={u.last_name} image_url={u.image_url}>"