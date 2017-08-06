"""Initiate the flask app."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from app.settings import Config
from app.register import register_apps, register_user_loader, \
                         register_request_hooks
from app.utils import generate_csrf_token


db = SQLAlchemy()


# Check http://flask.pocoo.org/docs/0.12/patterns/appfactories/
def create_app(config_object=Config):
    """Create the flask app instance."""
    # Initiate the flask instance with custom tempalte and static folders.
    flasko = Flask(__name__,
                   template_folder=config_object.template_folder,
                   static_folder=config_object.static_folder
                   )
    flasko.config.from_object(config_object)
    flasko.jinja_env.globals['csrf_token'] = generate_csrf_token

    # A flask_sqlalchemy wrapper that takes care of session creation/removal.
    from auth.models import User
    from catalog.models import Community, Pick
    db.init_app(flasko)

    # Bind the LoginManager to the app.
    login_manager = LoginManager()
    login_manager.init_app(flasko)
    register_user_loader(login_manager)

    # Register the rest of the apps (auth, catalog) and middlewares.
    register_apps(flasko)
    register_request_hooks(flasko)
    return flasko, db
