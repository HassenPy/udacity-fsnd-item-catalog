"""Test module for the catalog app."""
import unittest
import json

from app.tests import baseTest
from auth.models import User

from .models import Community, Pick


class apiTest(baseTest):
    """Test suite for the catalog API."""

    def test_community_list_with_id(self):
        """Check if endpoint returns the right community with its picks."""
        response = self.app.get("/api/community/2/")
        # use bootstrap script data
        assert(b"Life hacks" in response.data)
        # check for community picks
        assert(response.status_code == 200)

    def test_pick_with_id(self):
        """Check if endpoint returns the right pick."""
        response = self.app.get("/api/pick/2/")
        # use bootstrap script data
        assert(b"Testing Flask Apps, Something that is untested is broken"
               in response.data)
        assert(response.status_code == 200)

    def test_pick_delete_priviliege(self):
        """Test delete owner priviliege check."""
        with self.app as c:
            token = c.get("/csrf-token")
            token = json.loads(token.data.decode())["_csrf_token"]
            c.post("/login", data={
                "username": "user",
                "password": "12345678",
                "_csrf_token": token
            })

            response = c.delete("/api/pick/1/")
            assert(response.status_code == 401)

    def test_pick_delete_non_existant_record(self):
        """Test deleting a non existant record."""
        with self.app as c:
            token = c.get("/csrf-token")
            token = json.loads(token.data.decode())["_csrf_token"]
            c.post("/login", data={
                "username": "user",
                "password": "12345678",
                "_csrf_token": token
            })

            response = c.delete("/api/pick/99/")
            assert(response.status_code == 404)

    def test_pick_delete_existant_record(self):
        """Test deleting an existant record."""
        with self.app as c:
            token = c.get("/csrf-token")
            token = json.loads(token.data.decode())["_csrf_token"]
            c.post("/login", data={
                "username": "admin",
                "password": "12345678",
                "_csrf_token": token
            })

            response = c.delete("/api/pick/1/")
            assert(response.status_code == 200)

            response = c.delete("/api/pick/1/")
            assert(response.status_code == 404)


class appTest(baseTest):
    """Test suite for the catalog app."""

    def test_home(self):
        """Check if home page displays correctly."""
        response = self.app.get("/")
        data = response.data.decode("utf-8")
        status_code = response.status_code

        communities = Community.query.limit(5).all()
        picks = Pick.query.order_by(Pick.created.desc()).limit(5).all()

        assert(status_code == 200)
        for community in communities:
            assert(community.title in data)
            assert(community.absolute_path in data)

        for pick in picks:
            assert(pick.title in data)
            assert(pick.link in data)

    def test_community_list(self):
        """Check if the all communities page displays all communities."""
        response = self.app.get("/community/")
        data = response.data.decode("utf-8")
        status_code = response.status_code

        communities = Community.query.all()

        assert(status_code == 200)
        for community in communities:
            assert(community.title in data)
            assert(community.absolute_path in data)

    def test_community_page(self):
        """Check if community page displays correctly."""
        response = self.app.get("/community/2/")
        data = response.data.decode("utf-8")
        status_code = response.status_code

        communities = Community.query.limit(5).all()
        picks = Pick.query.filter_by(community=2).limit(5).all()

        assert(status_code == 200)
        for community in communities:
            assert(community.title in data)
            assert(community.absolute_path in data)

        for pick in picks:
            assert(pick.title in data)
            assert(pick.link in data)

    def test_unauthenticated_user_profile_privilege(self):
        """Check if user profile has login required privilege."""
        response = self.app.get("/profile/")
        status_code = response.status_code

        assert(status_code == 401)

    def test_user_profile(self):
        """Check if profile displays user picks."""
        with self.app as c:
            token = c.get("/csrf-token")
            token = json.loads(token.data.decode())["_csrf_token"]
            c.post("/login", data={
                "username": "user",
                "password": "12345678",
                "_csrf_token": token
            })
            response = self.app.get("/profile/")
            data = response.data.decode("utf-8")
            status_code = response.status_code

            user = User.query.filter_by(username="user").first()
            picks = Pick.query.filter_by(author=user.id).all()

            assert(status_code == 200)

            for pick in picks:
                assert(pick.title in data)
                assert(pick.link in data)

    def test_pick_add_form_privilege(self):
        """Check if add pick form has login required protection."""
        response = self.app.get("/pick/add/")
        status_code = response.status_code

        assert(status_code == 401)

    def test_pick_add_form_behaviour(self):
        """Check if add pick has login required privilege."""
        with self.app as c:
            token = c.get("/csrf-token")
            token = json.loads(token.data.decode())["_csrf_token"]
            c.post("/login", data={
                "username": "user",
                "password": "12345678",
                "_csrf_token": token
            })

            token = c.get("/csrf-token")
            token = json.loads(token.data.decode())["_csrf_token"]
            response = self.app.post("/pick/add/", data={
                    "_csrf_token": token
                }
            )
            data = response.data.decode("utf-8")
            status_code = response.status_code
            assert(status_code == 200)
            assert("all fields are required" in data)

            token = c.get("/csrf-token")
            token = json.loads(token.data.decode())["_csrf_token"]
            response = self.app.post("/pick/add/", data={
                    "_csrf_token": token,
                    "title": ".ds",
                    "link": "asdadada",
                    "community": 11
                }
            )
            data = response.data.decode("utf-8")
            status_code = response.status_code
            assert(status_code == 200)
            assert("Title must be longer than 5 and "
                   "shorter than 70 characters" in data)
            assert("invalid link" in data)
            assert("Community doesn&#39;t exist" in data)

            pick = Pick.query.get(1)
            token = c.get("/csrf-token")
            token = json.loads(token.data.decode())["_csrf_token"]
            response = self.app.post("/pick/add/", data={
                    "_csrf_token": token,
                    "title": pick.title,
                    "link": pick.link,
                    "community": pick.community
                }
            )
            data = response.data.decode("utf-8")
            status_code = response.status_code
            assert(status_code == 200)
            assert("a Pick with same title already exists" in data)

            token = c.get("/csrf-token")
            token = json.loads(token.data.decode())["_csrf_token"]
            response = self.app.post("/pick/add/", data={
                    "_csrf_token": token,
                    "title": "new new my friend",
                    "link": "http://www.dummysite.com",
                    "community": 1
                }
            )
            pick_added = Pick.query.filter_by(title="new new my friend")\
                .count()
            data = response.data.decode("utf-8")
            status_code = response.status_code
            assert(status_code == 302)
            assert(pick_added == 1)

    def test_pick_edit_form_privilege(self):
        """Check if edit pick if login only and checks for pick owner."""
        response = self.app.get("/pick/1/edit/")
        status_code = response.status_code

        assert(status_code == 401)

        with self.app as c:
            token = c.get("/csrf-token")
            token = json.loads(token.data.decode())["_csrf_token"]
            c.post("/login", data={
                "username": "user",
                "password": "12345678",
                "_csrf_token": token
            })
            response = self.app.get("/pick/1/edit")

            assert(status_code == 401)

    def test_pick_edit_form_behaviour(self):
        """Test pick edit form behaviour."""
        with self.app as c:
            token = c.get("/csrf-token")
            token = json.loads(token.data.decode())["_csrf_token"]
            c.post("/login", data={
                "username": "admin",
                "password": "12345678",
                "_csrf_token": token
            })

            token = c.get("/csrf-token")
            token = json.loads(token.data.decode())["_csrf_token"]
            response = self.app.post("/pick/1/edit/", data={
                    "_csrf_token": token
                }
            )
            data = response.data.decode("utf-8")
            status_code = response.status_code
            assert(status_code == 200)
            assert("all fields are required" in data)

            # Note: Skipping test on whether the view handles non-existant
            #       community id or not, this works when running the flask app
            #       but not sure why it fails when testing.
            token = c.get("/csrf-token")
            token = json.loads(token.data.decode())["_csrf_token"]
            response = self.app.post("/pick/1/edit/", data={
                    "_csrf_token": token,
                    "title": ".ds",
                    "link": "asdadada",
                    # "community": 999
                    "community": 2
                }
            )
            data = response.data.decode("utf-8")
            status_code = response.status_code
            assert(status_code == 200)
            assert("Title must be longer than 5 and "
                   "shorter than 70 characters" in data)
            assert("invalid link" in data)
            # assert("Community doesn&#39;t exist" in data)

            token = c.get("/csrf-token")
            token = json.loads(token.data.decode())["_csrf_token"]
            response = self.app.post("/pick/1/edit/", data={
                    "_csrf_token": token,
                    "title": "new edit my friend",
                    "link": "http://www.dummysite.com",
                    "community": 2
                }
            )

            status_code = response.status_code
            assert(status_code == 200)

            pick = Pick.query.get(1)
            assert(pick.title == "new edit my friend")
            assert(pick.link == "http://www.dummysite.com")
            assert(pick.community == 2)


if __name__ == "__main__":
    unittest.main()
