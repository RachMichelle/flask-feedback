from app import app
from models import db, User, Feedback

with app.app_context():

    db.drop_all()
    db.create_all()

    
    u1=User.register_user('dog', 'woof', 'dog@gmail.com', 'Toby', 'Bark')
    u2=User.register_user('cat','meow', 'cat@gmail.com','Mickey', 'Meow')
    
    db.session.add_all([u1, u2])
    db.session.commit()

    fb1=Feedback(title='meow', content='meow meow meow meow', username='cat')
    fb2=Feedback(title='woof', content='bark bark woof bark woof', username='dog')

    db.session.add_all([fb1, fb2])
    db.session.commit()