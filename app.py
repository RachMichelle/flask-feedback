from flask import Flask, render_template, redirect, session, flash, request
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedbackdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = 'feedbackapp'

connect_db(app)

@app.route('/')
def go_to_home():
    """no home page currently, redirects to register"""
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
        flash(f'Thanks for joining, {user.username}!')
        return redirect('/secret')    

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """search for existing user, log in if found and pwd correct"""

    form=LoginForm()

    if form.validate_on_submit():
        user=form.username.data
        pwd=form.password.data

        user=User.authenticate(user, pwd)

        if user:
            session['current_user']=user.username
            flash(f"Welcome back, {user.username}!", 'success')
            return redirect('/secret')
        else:
            flash("Invalid Username or Password", "danger")

    return render_template('login.html', form=form)

@app.route('/secret')
def show_secret():
    """secret page, only available when loggeed in"""
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

@app.route('/users/<username>')
def show_user_info(username):
    """shows user info page for associated username, only available to logged in users"""

    if session.get('current_user'):
        user = User.query.get_or_404(username)
        return render_template('user-info.html', user=user)
    else: 
        flash("You must be logged in to view that!", 'danger')
        return redirect('/login')
    
@app.route('/users/<username>/delete', methods=['GET', 'POST'])
def confirm_delete_account(username):
    """confirm deletion of account before proceeding"""

    user=User.query.get_or_404(username)

    if session.get('current_user') == user.username:
        if request.method == 'POST':
            user=User.query.filter_by(username=username).first()
            db.session.delete(user)
            db.session.commit()
            session.pop('current_user')
            return redirect('/')

        return render_template("confirm-delete.html", user=user)
    
    else:
        flash('You do not have permission to do that', 'danger')

        if session['current_user']:
            return redirect(f'/users/{session["current_user"]}')
        else: 
            return redirect('/')
        
@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    """add feedback associated with currently logged in user"""

    if not session['current_user']:
        flash('Please log in to post')
        return redirect('/login')

    if username != session['current_user']:
        flash('You do not have permission to do that')
        return redirect(f'/user/{session["current_user"]}')
    
    form=FeedbackForm()

    if form.validate_on_submit():
        title=form.title.data
        content=form.content.data
        username=username

        new_fb = Feedback.create_new_feedback(title, content, username)

        db.session.add(new_fb)
        db.session.commit()
        
        return redirect(f'/users/{username}')
    
    return render_template('feedback-add.html', form=form)

@app.route('/feedback/<feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    """update feedback at associated id if current user matches user associated with feedback"""

    if not session['current_user']:
        flash('You must be logged in to make edits')
        return redirect('/login')
    
    feedback=Feedback.query.get_or_404(feedback_id)

    if feedback.user.username != session['current_user']:
        flash('You do not have permission to do that')
        return redirect(f'/user/{session["current_user"]}')
    
    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title=form.title.data
        feedback.content=form.content.data

        db.session.commit()
        
        flash('Successfully Updated', "success")
        return redirect(f'/users/{feedback.user.username}')
    
    return render_template('feedback-edit.html', form=form)

@app.route('/feedback/<feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    """delete feedback at associated id if current user matches user associateed with feedback"""

    if not session['current_user']:
        flash('You must be logged in to make edits')
        return redirect('/login')
    
    feedback=Feedback.query.get_or_404(feedback_id)

    if feedback.user.username != session['current_user']:
        flash('You do not have permission to do that')
        return redirect(f'/user/{session["current_user"]}')
    
    Feedback.query.filter_by(id=feedback_id).delete()
    db.session.commit()

    flash('Successfully deleted', 'warning')
    return redirect(f'/users/{session["current_user"]}')