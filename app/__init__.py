"""Initiate the flask app."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app.settings import Config
from app.register import register_apps


flasko = Flask(__name__,
               template_folder=Config.template_folder,
               static_folder=Config.static_folder
               )
flasko.config.from_object(Config)
db = SQLAlchemy(flasko)
migrate = Migrate(flasko, db)

register_apps(flasko)
