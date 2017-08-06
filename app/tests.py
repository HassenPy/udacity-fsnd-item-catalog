"""Module for shared test classes."""
import unittest

from app import create_app
from app.settings import TestConfig
from bootstrap import bootstrap


class baseTest(unittest.TestCase):
    """Class that holds common test methods."""

    def setUp(self):
        """Initialize app and test db."""
        app, db = create_app(config_object=TestConfig)
        app.app_context().push()
        self.app = app.test_client()
        self.db = db
        bootstrap(app, db)

    def tearDown(self):
        """Destroy test db."""
        self.db.session.remove()
        self.db.drop_all()
