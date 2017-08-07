from uuid import uuid4
from flask import session


def generate_csrf_token():
    """Generate unique csrf token."""
    # from: http://flask.pocoo.org/snippets/3/
    if '_csrf_token' not in session:
        session['_csrf_token'] = uuid4().hex
    return session['_csrf_token']
