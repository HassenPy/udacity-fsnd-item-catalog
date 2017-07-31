"""Sub-package subscription logic for flask."""


def register_apps(flasko):
    """Subscribe apps to the flask instance."""
    from auth.views import authApp
    from catalog.views import catalogApp
    flasko.register_blueprint(authApp)
    flasko.register_blueprint(catalogApp)
