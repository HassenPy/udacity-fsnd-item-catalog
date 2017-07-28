"""Sub-package subscription logic for flask."""


def register_apps(flasko):
    """Subscribe apps to the flask instance."""
    from auth.views import authApp
    flasko.register_blueprint(authApp)
