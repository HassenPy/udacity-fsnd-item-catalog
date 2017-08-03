"""Settings for the flask app."""
import os
import json

base_dir = os.path.dirname(os.path.abspath(__file__))
fb_app = json.loads(open('app/fb_app.json', 'r').read())


class Config(object):
    """Base flask config."""

    SQLALCHEMY_DATABASE_URI = 'sqlite:///../sqlite.db'
    SECRET_KEY = ('\xb8\x03\x89\xffS\xa7v\xe78Z3\x15\xab\xfeT~\xf9!|3l'
                  '{\xa7\x18\x95\xf1\x17LfXQ;')
    DEBUG = True
    template_folder = os.path.join(os.path.dirname(base_dir),
                                   'templates')
    static_folder = os.path.join(os.path.dirname(base_dir),
                                 'static')
    domain = "http://localhost:5000"
    fb_app_id = fb_app['id']
    fb_app_secret = fb_app['secret']


class TestConfig(object):
    """Base flask config."""

    SQLALCHEMY_DATABASE_URI = 'sqlite:///../test.db'
    SECRET_KEY = 'd7af2b93103e488dbc55a08b7eca6176'
    DEBUG = True
    TESTING = True
    template_folder = os.path.join(os.path.dirname(base_dir),
                                   'templates')
    static_folder = os.path.join(os.path.dirname(base_dir),
                                 'static')
    domain = "http://localhost:5000"
