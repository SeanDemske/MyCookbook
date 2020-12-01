# run these tests like:
#
#    python -m unittest test_filename.py

import os
from unittest import TestCase

from models import db, connect_db, User, Recipe

os.environ["DATABASE_URL"] = "postgresql://postgres:developer@localhost:5432/mycookbook-test"

from app import app, CURR_USER_KEY

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class LandingPageTestCase(TestCase):
    """Tests for the homepage view"""

    def setUp(self):
        """Create test client"""

        User.query.delete()
        Recipe.query.delete()

        self.client = app.test_client()

        self.testuser = User.register("testuser", "tester@gmail.com", "password")

        db.session.commit()

    def test_homepage_display(self):
        """Is the data being displayed"""

        with self.client as c:
            resp = c.get("/")
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Your online cookbook!", str(resp.data))
            self.assertIn("How It Works", str(resp.data))

    def test_nav_signedout(self):
        """Tests the navbar display when signed out"""

        with self.client as c:
            resp = c.get("/")
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Sign In", str(resp.data))
            self.assertIn("Sign Up", str(resp.data))

    def test_nav_signedin(self):
        """Tests the navbar display when signed in"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.username

            resp = c.get("/")
            self.assertEqual(resp.status_code, 200)
            self.assertIn(self.testuser.username, str(resp.data))
            self.assertIn("Logout", str(resp.data))

    def test_profile_signedout(self):
        """Tests that a user is redirected if not signed in"""

        with self.client as c:
            resp = c.get(f"/{self.testuser.username}/cookbook")
            self.assertEqual(resp.status_code, 302)

    def test_profile_signedin(self):
        """Tests to make sure the correct info is being displayed when signed in"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.username

            resp = c.get(f"/{self.testuser.username}/cookbook")
            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"{self.testuser.username}\\\'s Recipes", str(resp.data))


    def test_signin_page_display(self):
        """Signin view function"""

        with self.client as c:
            resp = c.get("/login")
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Login", str(resp.data))
            self.assertIn("Username", str(resp.data))
            self.assertIn("Password", str(resp.data))

    def test_register_page_display(self):
        """Register view function"""

        with self.client as c:
            resp = c.get("/register")
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Register", str(resp.data))
            self.assertIn("Username", str(resp.data))
            self.assertIn("EMail", str(resp.data))
            self.assertIn("Password", str(resp.data))
            self.assertIn("Confirm Password", str(resp.data))