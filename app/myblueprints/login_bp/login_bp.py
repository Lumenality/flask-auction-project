from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from flask_bcrypt import Bcrypt
import json
from .login_repository import UserRepository, User

login_bp = Blueprint('login_bp', __name__,template_folder='templates')
user_repo = UserRepository()
    
#create the class for the login form
class LoginForm(FlaskForm):
    username = StringField('Användarnamn')
    password = PasswordField('Lösenord')
    submit = SubmitField('Logga in')
#create the class for the signup form
class SignupForm(FlaskForm):
    username = StringField('Användarnamn')
    email = StringField('Email')
    password = PasswordField('Lösenord')
    confirm_password = PasswordField('Bekräfta Lösenord')
    submit = SubmitField('Skapa användare')

#Initialize the flask-login extension
login_manager = LoginManager()#use in flask_app to init app
login_manager.login_view = 'login_bp.login'
#Initialize Bcrypt
bcrypt = Bcrypt()

@login_manager.user_loader #associates a function with Flask-Login to load user objects based on user IDs. It is a critical component of user session management and enables Flask-Login to recognize and manage user sessions effectively.
def load_user(user_id):
    # Load user from database
    user = user_repo.find_by_username(user_id)
    if user:
        return User(user.username, user.email, user.password_hash, user.role)
    else:
        return None

login_bp = Blueprint('login_bp', __name__, template_folder='templates')

@login_bp.route('/', methods=['GET'])
@login_required #Flask-Login checks whether the user is authenticated. If not Authenticated, they are not logged in, Flask-Login will typically redifect the user to a specified login page or location.
def secret():
    if current_user.is_authenticated:
        # Access the user's information
        username = current_user.username
        role = current_user.role
        logout_url = url_for('login_bp.logout')
        if role == 'admin':
            # redirect to index
            return redirect(url_for('admin'))
        if role == 'superuser':
            return f"Welcome Superuser {username}! This is a secret superuser page. <a href='{logout_url}'>Logout</a>"
        if role == 'user':
            return render_template('user_page.html', username=username, logout_url=logout_url)
    else:
        return redirect(url_for('login_bp.login'))

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = user_repo.find_by_username(username)
        print("Login: user found?", user)
        if not user:
            flash('No such username in database', 'danger')
            return render_template('login_form.html', form=form)
        if bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            if user.role == 'admin':
                return redirect(url_for('admin'))
            return redirect(url_for('index'))
        else:
            flash('Incorrect password', 'danger')
            return render_template('login_form.html', form=form)

    loginmessage = "Not logged in, to be able to add, delete or comment you myust be logged in with the right credentials"
    return render_template('login_form.html', form=form, loginmessage=loginmessage)

@login_bp.route('/signup', methods=['GET', 'POST'])
def create_user():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        password2 = form.confirm_password.data
        if password != password2:
            flash('Passwords do not match. Please try again.', 'danger')
            return render_template('create_user_form.html', form=form)
        existing_user = user_repo.find_by_username(username)
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return render_template('create_user_form.html', form=form)
        user_repo.add(username, email, user_repo.hash_password(password), role='user')
        flash('User created successfully. Please log in.', 'success')
        return redirect(url_for('login_bp.login'))
    return render_template('create_user_form.html', form=form)

@login_bp.route('/hashtest', methods=['GET','POST'])
def test_hash():
    if request.method == 'GET':
        return render_template('hashtest.html')
    password =  str(  (  (  (  request.form.get('password') ) ) ) )
    user_repo = UserRepository()
    hashed_password = user_repo.hash_password(password)
    flash(f'Hashed password: {hashed_password}', 'info')
    return render_template('hashtest.html', hashed_password=hashed_password)

@login_bp.route('/logout')
@login_required
def logout():
    logout_user()
    #flash('You have been logged out.')
    return redirect(url_for('index'))