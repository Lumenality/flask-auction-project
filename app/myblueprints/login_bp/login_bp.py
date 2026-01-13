from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from flask_bcrypt import Bcrypt
import json
from .login_repository import UserRepository, User

login_bp = Blueprint('login_bp', __name__,template_folder='templates')
user_repo = UserRepository()
    
#create the class for the form
class LoginForm(FlaskForm):
    username = StringField('Användarnamn')
    password = PasswordField('Lösenord')
    submit = SubmitField('Logga in')

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
    '''
    if role == 'admin' or role == 'superuser' or role == 'user':
        flash(F'Hello {current_user.username}, you are logged in with {current_user.role} credentials')
        return redirect(url_for('blog_bp.list_posts'))
        #return f"Welcome {current_user.username}! This is a secret page."
    '''

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = user_repo.find_by_username(username)
        # Load users from database
        if (not user):
            flash('No such username in database', 'danger')
            return render_template('login.html', form=form)
        
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)

            return redirect(url_for('login_bp.secret'))
        else:
            flash('Incorrect password', 'danger')
            return render_template('login.html', form=form)

    loginmessage = "Not logged in, to be able to add, delete or comment you myust be logged in with the right credentials"
    return render_template('login.html', form=form, loginmessage=loginmessage)

# @login_bp.route('/hashtest', methods=['GET'])
# def test_hash():
#     return render_template('hashtest.html')

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
    return redirect(url_for('login_bp.login'))