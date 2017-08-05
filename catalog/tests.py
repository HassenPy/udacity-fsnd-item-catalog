import unittest
import json

from app import create_app
from app.settings import TestConfig
from bootstrap import bootstrap


class authTest(unittest.TestCase):
    """Test suite for the auth app."""

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

    def test_category_list_with_id(self):
        """Check if endpoint returns the right category with its items."""
        response = self.app.get("/api/category/2/")
        # use bootstrap script data
        assert(b"Life hacks" in response.data)
        # check for category items
        assert(response.status_code == 200)

    def test_item_with_id(self):
        """Check if endpoint returns the right item."""
        response = self.app.get("/api/item/2/")
        # use bootstrap script data
        assert(b"Testing Flask Apps, Something that is untested is broken"
               in response.data)
        assert(response.status_code == 200)

    def test_item_delete_priviliege(self):
        """Test delete owner priviliege check."""
        with self.app as c:
            token = c.get('/csrf-token')
            token = json.loads(token.data.decode())['_csrf_token']
            c.post('/login', data={
                'username': 'user',
                'password': '12345678',
                '_csrf_token': token
            })

            response = c.delete('/api/item/1/')
            assert(response.status_code == 401)

    def test_item_delete_non_existant_record(self):
        """Test deleting a non existant record."""
        with self.app as c:
            token = c.get('/csrf-token')
            token = json.loads(token.data.decode())['_csrf_token']
            c.post('/login', data={
                'username': 'user',
                'password': '12345678',
                '_csrf_token': token
            })

            response = c.delete('/api/item/99/')
            assert(response.status_code == 404)

    def test_item_delete_existant_record(self):
        """Test deleting an existant record."""
        with self.app as c:
            token = c.get('/csrf-token')
            token = json.loads(token.data.decode())['_csrf_token']
            c.post('/login', data={
                'username': 'admin',
                'password': '12345678',
                '_csrf_token': token
            })

            response = c.delete('/api/item/1/')
            assert(response.status_code == 200)

            response = c.delete('/api/item/1/')
            assert(response.status_code == 404)


if __name__ == "__main__":
    unittest.main()
