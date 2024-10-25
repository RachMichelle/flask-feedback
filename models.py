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

    username=db.Column(db.String(20), primary_key=True, unique=True, nullable=False)

    password=db.Column(db.String(20), nullable=False)

    email=db.Column(db.String(50), nullable=False)

    first_name=db.Column(db.String(30), nullable=False)

    last_name=db.Column(db.String(30), nullable=False)

    def __repr__(self):
        u=self
        return f"<User- username: {u.username}, email: {u.email}, first/last name: {u.first_name} {u.last_name}>"
    
    @classmethod
    def register_user(cls, username, password, email, first_name, last_name):
        """hash pwd, create new User instance"""

        hash=bcrypt.generate_password_hash(password)
        hashed_str=hash.decode('utf8')

        return cls(username=username, password=hashed_str, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, password):
        """check for existing username, confirm matching pwd. Return instance of user or False"""

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

    def get_full_name(self):
        u=self
        return f'{u.first_name} {u.last_name}'


class Feedback(db.Model):
    """feedback model: id, title, post content, associated user"""

    __tablename__= "feedback"

    id=db.Column(db.Integer, primary_key=True, autoincrement=True)

    title=db.Column(db.String(100), nullable=False)

    content=db.Column(db.Text, nullable=False)

    username=db.Column(db.Text, db.ForeignKey('users.username'))

    user=db.relationship('User', backref='fb')

    def __repr__(self):
        fb=self
        return f'<id: {fb.id}, title: {fb.title}, content: {fb.content}, posted by {fb.username}'