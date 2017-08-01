"""Settings for the flask app."""
import os

base_dir = os.path.dirname(os.path.abspath(__file__))


class Config(object):
    """Base flask config."""

    SQLALCHEMY_DATABASE_URI = 'sqlite:///../sqlite.db'
    SECRET_KEY = '\xb8\x03\x89\xffS\xa7v\xe78Z3\x15\xab\xfeT~\xf9!|3l{\xa7\x18\x95\xf1\x17LfXQ;'
    DEBUG = True
    template_folder = os.path.join(os.path.dirname(base_dir),
                                   'templates')
    static_folder = os.path.join(os.path.dirname(base_dir),
                                 'static')
    domain = "http://127.0.0.1:5000"


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
    domain = "http://127.0.0.1:5000"
