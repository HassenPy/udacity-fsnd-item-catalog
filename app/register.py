"""Sub-package subscription logic for flask."""


def register_apps(flasko):
    """Subscribe apps to the flask instance."""
    from auth.views import authApp
    from catalog.views import catalogApp
    flasko.register_blueprint(authApp)
    flasko.register_blueprint(catalogApp)


def register_middlewares(flasko):
    """Import flask middlewares."""
    from app import middlewares
    flasko.jinja_env.globals['csrf_token'] = middlewares.generate_csrf_token
