"""Settings for the flask app."""
import os
import json

base_dir = os.path.dirname(os.path.abspath(__file__))
fb_app = json.loads(open('app/fb_app.json', 'r').read())


class Config(object):
    """Base flask config."""

    SQLALCHEMY_DATABASE_URI = 'postgresql:///pickydb'
    SECRET_KEY = os.environ['SECRET_KEY']
    DEBUG = True
    template_folder = os.path.join(os.path.dirname(base_dir),
                                   'templates')
    static_folder = os.path.join(os.path.dirname(base_dir),
                                 'static')
    SERVER_NAME = "localhost:5000"
    fb_app_id = fb_app['id']
    fb_app_secret = fb_app['secret']
    SESSION_COOKIE_NAME = "sid"


class TestConfig(object):
    """Base flask config."""

    SQLALCHEMY_DATABASE_URI = 'postgresql:///pickydbtest'
    SECRET_KEY = os.environ['SECRET_KEY']
    DEBUG = True
    TESTING = True
    template_folder = os.path.join(os.path.dirname(base_dir),
                                   'templates')
    static_folder = os.path.join(os.path.dirname(base_dir),
                                 'static')
    SERVER_NAME = "localhost:5000"
    SESSION_COOKIE_NAME = "sid"
