"""Test module for the auth app."""
import unittest
import json

from app.tests import baseTest


class authTest(baseTest):
    """Test suite for the auth app."""

    def test_unauthenticated_login_page_render(self):
        """Login page unauthenticated user page display test."""
        response = self.app.get("/login")
        assert(response.status_code == 200)

    def test_authenticated_login_page_redirect(self):
        """Login page authenticated user page redirect test."""
        with self.app as c:
            token = c.get('/csrf-token')
            token = json.loads(token.data.decode())['_csrf_token']
            response = c.post('/login', data={
                'username': 'user',
                'password': '12345678',
                '_csrf_token': token
            })
            response = self.app.get("/login")
            assert(response.status_code == 302)

    def test_login_form_csrf_protection(self):
        """Login form csrf protection test."""
        response = self.app.post('/login', data={
            'username': 'user',
            'password': '12345678'
        })
        assert(response.status_code == 403)

    def test_login_form_post_success(self):
        """Valid data login form post test."""
        with self.app as c:
            token = c.get('/csrf-token')
            token = json.loads(token.data.decode())['_csrf_token']
            response = c.post('/login', data={
                'username': 'user',
                'password': '12345678',
                '_csrf_token': token
            })
            assert(response.status_code == 302)

    def test_login_form_error(self):
        """Erronous data login form post test."""
        with self.app as c:
            token = c.get('/csrf-token')
            token = json.loads(token.data.decode())['_csrf_token']
            response = c.post('/login', data={
                'username': '',
                'password': '',
                '_csrf_token': token
            })
            assert(b"Please provide login credentials!" in response.data)

            token = c.get('/csrf-token')
            token = json.loads(token.data.decode())['_csrf_token']
            response = c.post('/login', data={
                'username': 'user',
                'password': '1234',
                '_csrf_token': token
            })
            assert(b"Unvalid credentials." in response.data)

    def test_unauthenticated_logout(self):
        """Unauthenticated user logout test."""
        response = self.app.get("/logout")
        assert(response.status_code == 401)

    def test_authenticated_logout(self):
        """Authenticated user logout test."""
        with self.app as c:
            token = c.get('/csrf-token')
            token = json.loads(token.data.decode())['_csrf_token']
            response = c.post('/login', data={
                'username': 'user',
                'password': '12345678',
                '_csrf_token': token
            })
            response = self.app.get("/logout")
            assert(response.status_code == 302)

    def test_unauthenticated_signup_page_render(self):
        """Signup page unauthenticated user page display test."""
        response = self.app.get("/signup")
        assert(response.status_code == 200)

    def test_authenticated_signup_page_redirect(self):
        """Signup page redirects authenticated user."""
        with self.app as c:
            token = c.get('/csrf-token')
            token = json.loads(token.data.decode())['_csrf_token']
            c.post('/login', data={
                'username': 'user',
                'password': '12345678',
                '_csrf_token': token
            })
            response = c.get('/signup')
            assert(response.status_code == 302)

    def test_signup_form_csrf_protection(self):
        """Login form csrf protection test."""
        response = self.app.post('/signup', data={
            'username': 'user2',
            'password': '12345678',
            'email': 'hassenbtn@gmail.com',
            'email1': 'hassenbtn@gmail.com',
        })
        assert(response.status_code == 403)

    def test_signup_form_post_success(self):
        """Test signup form with valid data."""
        with self.app as c:
            token = c.get('/csrf-token')
            token = json.loads(token.data.decode())['_csrf_token']
            response = c.post('/signup', data={
                'username': 'user23',
                'password': '12345678',
                'email': 'hassenbtn@gmail.com',
                'emailConfirm': 'hassenbtn@gmail.com',
                '_csrf_token': token
            })
            assert(b"You are now a member of the Picky! community." in
                   response.data)

    def test_signup_form_error(self):
        """Test signup form with erronous data."""
        with self.app as c:
            token = c.get('/csrf-token')
            token = json.loads(token.data.decode())['_csrf_token']
            response = c.post('/signup', data={
                'username': '~!',
                'password': '~!',
                'email': 'hassenbtn',
                'emailConfirm': 'hassenbtn@gmail.com',
                '_csrf_token': token
            })
            assert(b"username must only use alphanumerics." in response.data)
            assert((b"username must be longer than 3 and " +
                   b"shorter than 12 characters") in response.data)
            assert(b"email is invalid." in response.data)
            assert(b"emails do not match." in response.data)
            assert(b"password must be at least 8 characters long."
                   in response.data)
            assert(b"Password cannot be the same as your username."
                   in response.data)


if __name__ == "__main__":
    unittest.main()
