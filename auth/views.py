"""Authentication views."""
from flask import Blueprint, request, render_template

from app import db

from .models import User

authApp = Blueprint('authApp', __name__)


@authApp.route('/signup', methods=['GET', 'POST'])
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
