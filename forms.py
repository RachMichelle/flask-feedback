from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length

class RegisterForm(FlaskForm):
    """Registration form for new users--username, pwd, email, first&last name"""

    username=StringField("Username", validators=
                         [InputRequired(message="Required"), Length(max=20, message="Must be less than 20 characters")])

    password=PasswordField("Password", validators=
                         [InputRequired(message="Required"), Length(min=6, max=20, message="Must be between 6-20 characters in length")])
    
    email=StringField("Email Address", validators=
                      [InputRequired(message="Please enter a valid email address")])
    
    first_name=StringField("First Name", validators=
                           [InputRequired(message="Required"), Length(max=30, message="Must be less than 30 characters in length")])
    
    last_name=StringField("Last Name", validators=
                          [InputRequired(message="Required"), Length(max=30, message="Must be less than 30 characters in length")])
    
class LoginForm(FlaskForm):
    """login form for existing users--username, pwd"""

    username=StringField("Username", validators=
                         [InputRequired(message="Required")])
    
    password=PasswordField("Password", validators=
                           [InputRequired(message="Required")])
    
class FeedbackForm(FlaskForm):
    """form to add and edit feedback"""

    title=StringField("Title", validators=
                      [InputRequired(message="Required"), Length(max=100, message='Title cannot be longer than 100 characters')])
    
    content=StringField("Content", validators=
                        [InputRequired(message="Required")])