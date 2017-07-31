"""Authentication views."""
from uuid import uuid4
from flask import Blueprint, request, render_template, redirect, \
                  session, jsonify
from flask_login import login_user, login_required, logout_user

from app import db, login_manager

from .models import User
from .utils import logout_required

authApp = Blueprint('authApp', __name__)


@login_manager.user_loader
def load_user(user_id):
    """Tell flask-login what query to use to get the user with his id."""
    return User.query.get(user_id)


@authApp.route('/', methods=['GET'])
def home():
    """Home page."""
    return render_template('home.html')


@authApp.route('/signup', methods=['GET', 'POST'])
@logout_required
def signup():
    """Signup page view."""
    if request.method == 'POST':
        user = User(
            username=request.form['username'],
            password=request.form['password'],
            email=request.form['email'],
            email1=request.form['emailConfirm']
        )
        # Use the user model to validate the form data.
        if user.is_valid():
            # Generate user password and commit changes to db.
            user.make_password()
            db.session.add(user)
            db.session.commit()
            return signup_success()
        return render_template('signup.html', errors=user.errors)
    return render_template('signup.html', errors=None)


def signup_success():
    """Render the singup success page."""
    message = {
        'type': 'success',
        'header': 'Congratulations!',
        'body': 'You are now a member of the Picky! community.'
    }
    return render_template("message.html", message=message)


@authApp.route('/login', methods=['GET', 'POST'])
@logout_required
def login():
    """Login management view."""
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if not (username or password):
            return render_template(
                'login.html',
                error="Please provide login credentials!"
            )
        user = User.query.filter_by(username=username).first()
        if not user:
            return render_template(
                'login.html',
                error="Unvalid login credentials!"
            )
        try:
            user.verify_password(password)
            login_user(user)
            return redirect('/')
        except Exception as e:
            return render_template('login.html', error=e.args[0])
    return render_template('login.html', error=None)


@authApp.route("/logout", methods=['GET'])
@login_required
def logout():
    """Logout and redirect to home page."""
    logout_user()
    return redirect('/')


@authApp.route("/csrf-token", methods=['GET'])
def get_csrf():
    """Generate randomly unique csrf token for API POST requests."""
    # from: http://flask.pocoo.org/snippets/3/
    if '_csrf_token' not in session:
        session['_csrf_token'] = uuid4().hex
    return jsonify({'_csrf_token': session['_csrf_token']})
