from flask import Flask, render_template, redirect
from models import db, connect_db, User
from forms import RegisterForm, LoginForm


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
    form=RegisterForm()
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    form=LoginForm()
    return render_template('login.html', form=form)

@app.route('/secret')
def show_secret():
    return render_template ('secret.html')