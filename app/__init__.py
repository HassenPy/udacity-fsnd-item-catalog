"""Initiate the flask app."""
from uuid import uuid4
from flask import Flask, session, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from app.settings import Config
from app.register import register_apps


def generate_csrf_token():
    """Generate randomly unique csrf token."""
    # from: http://flask.pocoo.org/snippets/3/
    if '_csrf_token' not in session:
        session['_csrf_token'] = uuid4().hex
    return session['_csrf_token']


# Initiate the flask instance with custom tempalte and static folders.
flasko = Flask(__name__,
               template_folder=Config.template_folder,
               static_folder=Config.static_folder
               )
flasko.config.from_object(Config)
flasko.jinja_env.globals['csrf_token'] = generate_csrf_token

# A flask_sqlalchemy wrapper that takes care of session creation/removal.
db = SQLAlchemy(flasko)

# Bind the LoginManager to the app.
login_manager = LoginManager()
login_manager.init_app(flasko)

# Register the rest of the apps (auth, items).
register_apps(flasko)


@flasko.before_request
def csrf_protect():
    """Bind a crf token check before a request is sent to a view."""
    # from: http://flask.pocoo.org/snippets/3/
    if request.method == "POST":
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)
