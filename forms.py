from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, NumberRange, Email

class RegisterForm(FlaskForm):
    """Registration form for new users--username, pwd, email, first&last name"""

    username=StringField("Username", validators=
                         [InputRequired(message="Required"), NumberRange(max=20, message="Must be less than 20 characters")])

    password=PasswordField("Password", validators=
                         [InputRequired(message="Required"), NumberRange(min=6, max=20, message="Must be between 6-20 characters in length")])
    
    email=StringField("Email Address", validators=
                      [InputRequired(message="Please enter a valid email address"), Email(message="Please enter a valid email address")])
    
    first_name=StringField("First Name", validators=
                           [InputRequired(message="Required"), NumberRange(max=30, message="Must be less than 30 characters in length")])
    
    last_name=StringField("Last Name", validators=
                          [InputRequired(message="Required"), NumberRange(max=30, message="Must be less than 30 characters in length")])
    
class LoginForm(FlaskForm):
    """login form for existing users--username, pwd"""

    username=StringField("Username", validators=
                         [InputRequired(message="Required")])
    
    password=PasswordField("Password", validators=
                           [InputRequired(message="Required")])