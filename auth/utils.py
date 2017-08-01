"""User authentication utility functions."""
from functools import wraps
from flask import session, redirect, url_for, abort

from .models import User


def logout_required(f):
    """Redirects if user accesses a page when logged in."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        logged_in = session.get('user_id', False)
        if logged_in:
            return redirect(url_for('authApp.home'))
        return f(*args, **kwargs)
    return decorated_function


def is_admin(f):
    """Check user permissions."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        user_id = session.get('user_id', False)
        if user_id:
            is_admin = User.query.get(user_id).is_admin()
            if not is_admin:
                abort(401)
        return f(*args, **kwargs)
    return wrapper
