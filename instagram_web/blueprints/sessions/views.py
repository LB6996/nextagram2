from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required
from instagram_web.util.google_oauth import oauth

sessions_blueprint = Blueprint('sessions',
                                __name__,
                                template_folder='templates')


@sessions_blueprint.route('/login', methods=['GET'])
def login():
    return render_template('sessions/login.html')


@sessions_blueprint.route('/', methods=['POST'])
def create():
    username = request.form.get('username')
    user = User.get_or_none(User.username == username)
    if user != None:
        password = request.form.get('password')
        result = check_password_hash(user.password, password)
        if result == True:
            login_user(user)
            flash(f'Welcome back, {username}!', 'alert alert-success')
            return redirect(url_for('home'))
        else:
            flash('Username and/or password doesn\'t match out records!', 'alert alert-danger')
            return render_template('sessions/login.html')
    else: 
        flash('Username and/or password doesn\'t match out records!', 'alert alert-danger')
        return render_template('sessions/login.html')

@sessions_blueprint.route('/google_login')
def google_login():
    redirect_uri = url_for('sessions.authorize', _external = True)
    return oauth.google.authorize_redirect(redirect_uri)

@sessions_blueprint.route('/authorize/google')
def authorize():
    oauth.google.authorize_access_token()
    email = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
    user = User.get_or_none(User.email == email)
    if user:
        login_user(user)
        flash('Successfully logged in with Google.','alert alert-success')
        return redirect(url_for('home'))
    else:
        flash('Login failed.','alert alert-danger')
        return render_template('sessions/login.html')


@sessions_blueprint.route('/logout')
def logout():
    logout_user()
    flash('Successfully logged out!','alert alert-success')
    return redirect(url_for('sessions.login'))

