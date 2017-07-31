"""Request--Response cycle and template hooks."""
from uuid import uuid4
from flask import request, session, abort

from app import flasko


@flasko.before_request
def csrf_protect():
    """Bind a crf token check before a request is sent to a view."""
    # from: http://flask.pocoo.org/snippets/3/
    if request.method == "POST":
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)


def generate_csrf_token():
    """Generate randomly unique csrf token."""
    # from: http://flask.pocoo.org/snippets/3/
    if '_csrf_token' not in session:
        session['_csrf_token'] = uuid4().hex
    return session['_csrf_token']
