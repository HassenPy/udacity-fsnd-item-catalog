"""Initiate the flask app."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from app.settings import Config
from app.register import register_apps, register_middlewares


# Initiate the flask instance with custom tempalte and static folders.
flasko = Flask(__name__,
               template_folder=Config.template_folder,
               static_folder=Config.static_folder
               )
flasko.config.from_object(Config)

# A flask_sqlalchemy wrapper that takes care of session creation/removal.
db = SQLAlchemy(flasko)

# Bind the LoginManager to the app.
login_manager = LoginManager()
login_manager.init_app(flasko)

# Register the rest of the apps (auth, catalog) and middlewares.
register_apps(flasko)
register_middlewares(flasko)
