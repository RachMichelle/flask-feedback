from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """connect to database"""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """user model: username, password, email, first&last name"""

    __tablename__= 'users'

    username=db.Column(db.Text(20), primary_key=True, unique=True, nullable=False)

    password=db.Column(db.Text(20), nullable=False)

    email=db.Column(db.Text(50), nullable=False)

    first_name=db.Column(db.Text(30), nullable=False)

    last_name=db.Column(db.Text(30), nullable=False)

    def __repr__(self):
        u=self
        return f"<User- username: {u.username}, email: {u.email}, first/last name: {u.first_name} {u.last_name}>"
    

class Feedback(db.Model):
    """feedback model: id, title, post content, associated user"""

    __tablename__= "feedback"

    id=db.Column(db.Integer, primary_key=True, autoincrement=True)

    title=db.Column(db.Text(100), nullable=False)

    content=db.Column(db.Text, nullable=False)

    username=db.Column(db.Text, db.ForeignKey('users.username'))

    user=db.relationship('User', backref='fb')

    def __repr__(self):
        fb=self
        return f'<id: {fb.id}, title: {fb.title}, content: {fb.content}, posted by {fb.username}'