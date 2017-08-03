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

    def test_category_list_without_id(self):
        """
        Check if endpoint returns a list of categories when no id provided.
        """
        response = self.app.get("/catalog/category/")
        # use bootstrap script data
        assert(b"Computer stuff" in response.data)
        assert(b"Life hacks" in response.data)
        assert(response.status_code == 200)

    def test_category_list_with_id(self):
        """Check if endpoint returns the right category with its items."""
        response = self.app.get("/catalog/category/2/")
        # use bootstrap script data
        assert(b"Life hacks" in response.data)
        # check for category items
        assert(b"facebook" in response.data)
        assert(b"twitter" in response.data)
        assert(response.status_code == 200)

    def test_category_post_csrf_protection(self):
        """Check if endpoint is csrf protected."""
        response = self.app.post('/catalog/category/', data={
        })
        assert(response.status_code == 403)

    def test_category_unauthenticated_post(self):
        """Check if endpoint is login only."""
        with self.app as c:
            token = c.get('/csrf-token')
            token = json.loads(token.data.decode())['_csrf_token']
            response = c.post('/catalog/category/', data={
                '_csrf_token': token
            })
            assert(response.status_code == 401)

    def test_category_post_user_priviliege(self):
        """Check if endpoint rejects non admin posts."""
        with self.app as c:
            token = c.get('/csrf-token')
            token = json.loads(token.data.decode())['_csrf_token']
            c.post('/login', data={
                'username': 'user',
                'password': '12345678',
                '_csrf_token': token
            })

            token = c.get('/csrf-token')
            token = json.loads(token.data.decode())['_csrf_token']
            response = c.post('/catalog/category/', data={
                '_csrf_token': token
            })
            assert(response.status_code == 401)

    def test_category_post_data(self):
        """Check endpoint data validation."""
        with self.app as c:
            token = c.get('/csrf-token')
            token = json.loads(token.data.decode())['_csrf_token']
            c.post('/login', data={
                'username': 'admin',
                'password': '12345678',
                '_csrf_token': token
            })

            # Check for required params
            token = c.get('/csrf-token')
            token = json.loads(token.data.decode())['_csrf_token']
            response = c.post('/catalog/category/', data={
                'title': 'yo',
                '_csrf_token': token
            })
            assert(response.status_code == 400)

            # Check for erronous params
            token = c.get('/csrf-token')
            token = json.loads(token.data.decode())['_csrf_token']
            response = c.post('/catalog/category/', data={
                'title': 'yo',
                '_csrf_token': token
            })
            assert(response.status_code == 400)

            # Check for existing category
            token = c.get('/csrf-token')
            token = json.loads(token.data.decode())['_csrf_token']
            response = c.post('/catalog/category/', data={
                'title': 'Life hacks',
                'description': 'new description',
                '_csrf_token': token
            })
            assert(response.status_code == 409)

    def test_category_put_user_priviliege(self):
        """Check if endpoint rejects non admin updates."""
        with self.app as c:
            token = c.get('/csrf-token')
            token = json.loads(token.data.decode())['_csrf_token']
            c.post('/login', data={
                'username': 'user',
                'password': '12345678',
                '_csrf_token': token
            })

            response = c.put('/catalog/category/1/', data={
                'title': 'Oh i changed :/'
            })
            assert(response.status_code == 401)

    def test_category_put_data(self):
        """Check endpoint data validation."""
        with self.app as c:
            token = c.get('/csrf-token')
            token = json.loads(token.data.decode())['_csrf_token']
            c.post('/login', data={
                'username': 'admin',
                'password': '12345678',
                '_csrf_token': token
            })

            # Missing required parameter
            response = c.put('/catalog/category/1/')
            assert(response.status_code == 400)

            # Check for erronous params
            response = c.put('/catalog/category/1/', data={
                'title': 'yo',
            })
            assert(response.status_code == 400)

            # Check for non existing category
            response = c.put('/catalog/category/999/')
            assert(response.status_code == 404)

    def test_category_delete_priviliege(self):
        """Test delete admin priviliege check."""
        with self.app as c:
            token = c.get('/csrf-token')
            token = json.loads(token.data.decode())['_csrf_token']
            c.post('/login', data={
                'username': 'user',
                'password': '12345678',
                '_csrf_token': token
            })

            response = c.delete('/catalog/category/1/')
            assert(response.status_code == 401)

    def test_category_delete_non_existant_record(self):
        """Test deleting a non existant record."""
        with self.app as c:
            token = c.get('/csrf-token')
            token = json.loads(token.data.decode())['_csrf_token']
            c.post('/login', data={
                'username': 'admin',
                'password': '12345678',
                '_csrf_token': token
            })

            response = c.delete('/catalog/category/99/')
            assert(response.status_code == 404)

    def test_category_delete_existant_record(self):
        """Test deleting an existant record."""
        with self.app as c:
            token = c.get('/csrf-token')
            token = json.loads(token.data.decode())['_csrf_token']
            c.post('/login', data={
                'username': 'admin',
                'password': '12345678',
                '_csrf_token': token
            })

            response = c.delete('/catalog/category/1/')
            assert(response.status_code == 200)

            response = c.delete('/catalog/category/1/')
            assert(response.status_code == 404)


if __name__ == "__main__":
    unittest.main()
