from flask import Flask, render_template, redirect
from models import db, connect_db, User


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedbackdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

connect_db(app)

@app.route('/')
def go_to_home():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    return render_template('login.html')

@app.route('/secret')
def show_secret():
    return render_template ('secret.html')