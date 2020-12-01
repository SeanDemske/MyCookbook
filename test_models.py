# run these tests like:
#
#    python -m unittest test_filename.py

import os
from unittest import TestCase
from sqlalchemy import exc, orm

from models import db, User, Recipe

os.environ["DATABASE_URL"] = "postgresql://postgres:developer@localhost:5432/mycookbook-test"

from app import app

db.create_all()

class UserModelTestCase(TestCase):
    """Test model functionality"""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Recipe.query.delete()

        self.testuser = User.register("testuser", "tester@gmail.com", "password")
        self.testrecipe = Recipe(title="Test Recipe", ingredient_list="Test Ingredient", cookbook_owner="testuser")

        db.session.add(self.testuser)
        db.session.add(self.testrecipe)
        db.session.commit()

        self.client = app.test_client()

    def test_user_model(self):
        """Basic model creation"""

        self.assertEqual(self.testuser.username, "testuser")
        self.assertEqual(self.testuser.email, "tester@gmail.com")

    def test_authentication(self):
        """Tests the authentication functionality"""

        self.assertEqual(str(User.authenticate("testuser", "password")), f"<User {self.testuser.username}: {self.testuser.email}>")
        self.assertEqual(User.authenticate("incorrect_username", "password"), False)
        self.assertEqual(User.authenticate("authenticated_user", "incorrect_password"), False)

    def test_recipe_model(self):
        """Basic model creation"""

        self.assertEqual(self.testrecipe.title, "Test Recipe")
        self.assertEqual(self.testrecipe.ingredient_list, "Test Ingredient")
        self.assertEqual(self.testrecipe.cookbook_owner, "testuser")

    def test_user_recipe_relationship(self):
        """User/Recipe relationship"""

        testuser_recipes = Recipe.query.filter_by(cookbook_owner=self.testuser.username).all()
        self.assertEqual(len(testuser_recipes), 1)
        self.assertEqual(testuser_recipes[0].title, "Test Recipe")
        self.assertEqual(testuser_recipes[0].cookbook_owner, self.testuser.username)

