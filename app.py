from flask import Flask, render_template, redirect, session, flash
from models import db, connect_db, User
from forms import RegisterForm, LoginForm
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedbackdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = 'feedbackapp'

connect_db(app)

@app.route('/')
def go_to_home():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    """create new User instance and add to db, keep logged in"""

    form=RegisterForm()

    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        email=form.email.data
        first_name=form.first_name.data
        last_name=form.last_name.data

        user=User.register_user(username, password, email, first_name, last_name)
        
        db.session.add(user)

        try:
            db.session.commit()
        
        except IntegrityError:
            form.username.errors.append('Username not available')
            return render_template('/register.html', form=form)
        
        session['current_user']=user.username
        return redirect('/secret')    

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """search for existing user, log in if found and pwd correct"""
    form=LoginForm()

    if form.validate_on_submit():
        user=form.username.data
        pwd=form.password.data

        User.authenticate(user, pwd)

        if user:
            session['current_user']=user.username
            flash(f"Welcome back, {user.username}!", 'success')
            return redirect('/secret')
        else:
            flash("Invalid Username or Password", "danger")

    return render_template('login.html', form=form)

@app.route('/secret')
def show_secret():
    if session.get('current_user'):
        return render_template ('secret.html')
    else:
        flash("You must be logged in to view that!", 'danger')
        return redirect('/login')

@app.route('/logout', methods=['POST'])
def logout_user():
    """log out current user"""
    session.pop('current_user')
    return redirect('/login')
