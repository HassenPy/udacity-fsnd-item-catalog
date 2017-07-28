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
    apps = [
        'auth',
    ]
