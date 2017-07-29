"""User authentication utility functions."""
from functools import wraps
from flask import session, redirect, url_for


def logout_required(f):
    """Redirects if user accesses a page when logged in."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print("Checking privilege!")
        logged_in = session.get('user_id', False)
        if logged_in:
            print("Gonna redirect!")
            return redirect(url_for('authApp.home'))
        print("seems fine!")
        return f(*args, **kwargs)
    return decorated_function
