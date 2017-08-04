"""Application apps and hooks registration logic."""
from flask import request, session, abort


def register_apps(flasko):
    """Subscribe apps to the flask instance."""
    from auth.views import authApp
    from auth.api import authAPI
    from catalog.views import catalogApp
    from catalog.api import catalogAPI
    flasko.register_blueprint(authApp)
    flasko.register_blueprint(authAPI)
    flasko.register_blueprint(catalogApp)
    flasko.register_blueprint(catalogAPI)


def register_user_loader(login_manager):
    """Register required user loader for the flask-login dependency."""
    from auth.models import User

    @login_manager.user_loader
    def load_user(user_id):
        """Tell flask-login what query to use to get the user with his id."""
        return User.query.get(user_id)


def register_request_hooks(app):
    """Register hooks that run at certain stages of the request cycle."""
    @app.before_request
    def csrf_protect():
        """Bind a crf token check before a request is sent to a view."""
        # from: http://flask.pocoo.org/snippets/3/
        if request.method == "POST":
            token = session.pop('_csrf_token', None)
            if not token or token != request.form.get('_csrf_token'):
                abort(403)
