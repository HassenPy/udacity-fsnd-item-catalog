"""User authentication utility functions."""
import requests
from functools import wraps
from flask import session, redirect, url_for, abort

from app.settings import Config

from .models import User


def get_fb_user(access_token):
    """Get facebook user access_token and fetch user data."""
    app_id = Config.fb_app_id
    app_secret = Config.fb_app_secret
    url = ("https://graph.facebook.com/oauth/access_token?"
           "grant_type=fb_exchange_token&client_id=%s&client_secret=%s"
           "&fb_exchange_token=%s" % (app_id, app_secret, access_token))
    token = requests.get(url).json()
    url = ("https://graph.facebook.com/v2.10/me/"
           "?access_token=%s&fields=name,id,email" % token["access_token"])
    response = requests.get(url).json()
    return response


def logout_required(f):
    """Decorator that redirects if user accesses a page when logged in."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        logged_in = session.get("user_id", False)
        if logged_in:
            return redirect(url_for("catalogApp.home"))
        return f(*args, **kwargs)
    return decorated_function


def is_admin(f):
    """Decorator that checks if user is admin."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        user_id = session.get("user_id", False)
        if user_id:
            is_admin = User.query.get(user_id).is_admin()
            if not is_admin:
                abort(401)
        return f(*args, **kwargs)
    return wrapper
