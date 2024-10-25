from app import app
from models import db, User, Feedback

with app.app_context():

    db.drop_all()
    db.create_all()

    u1=User(username='dog', password='woof', email='dog@gmail.com', first_name='Toby', last_name='Bark')
    u2=User(username='cat', password='meow', email='cat@gmail.com', first_name='Mickey', last_name='Meow')
    
    db.session.add_all([u1, u2])
    db.session.commit()

    # fb1=Feedback(title='meow', content='meow meow meow meow', username='cat')
    # fb2=Feedback(title='woof', content='bark bark woof bark woof', username='dog')

    # db.session.add_all([fb1, fb2])
    # db.session.commit()