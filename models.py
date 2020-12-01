"""Models for User and Recipes"""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from utilities import recipe_list_to_string

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """Connect to database"""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User"""

    __tablename__ = "users"

    username = db.Column(db.String(20),
                    primary_key=True,
                    nullable=False,
                    unique=True)
    password = db.Column(db.Text,
                    nullable=False)
    email = db.Column(db.Text,
                    nullable=True,
                    unique=True)

    recipes = db.relationship("Recipe",
                    backref="user",
                    lazy='dynamic'
    )

    def __repr__(self):
        return f"<User {self.username}: {self.email}>"

    def add_recipe(self, recipe, username):
        "Takes a dictionary and pulls the data to create a recipe instance and appends it to the user(self)"

        ingredients = recipe_list_to_string(recipe.get("ingredientLines"))

        return Recipe(
            title=recipe.get("label", "Error"),
            recipe_image_url=recipe.get("image", "/static/images/recipe_placeholder.png"),
            source_url=recipe.get("url", "Source not found"),
            servings=recipe.get("yield", "NA"),
            calories=recipe.get("calories", "---"),
            total_minutes=recipe.get("totalTime", "NA"),
            ingredient_list=ingredients,
            cookbook_owner=username
        )

        

    @classmethod
    def register(cls, username, email, password):
        """Creates a new user and adds it to the database. Returns user instance"""

        hashed_password = bcrypt.generate_password_hash(password).decode("UTF-8")
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)

        return user

    @classmethod
    def authenticate(cls, username, password):
        """Athenticates login credentials"""

        user = cls.query.filter_by(username=username).first()
        if not user:
            return False

        if bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

    
class Recipe(db.Model):
    """Recipe"""

    __tablename__ = "recipes"

    id = db.Column(db.Integer,
                    autoincrement=True,
                    primary_key=True)
    title = db.Column(db.String(50),
                    nullable=False,
                    unique=True)
    recipe_image_url = db.Column(db.Text,
                    default="/static/images/recipe_placeholder.png")
    source_url = db.Column(db.Text,
                    nullable=True)
    servings = db.Column(db.Integer,
                    nullable=True)
    calories = db.Column(db.Integer,
                    nullable=True)
    total_minutes = db.Column(db.Integer,
                    nullable=True)
    ingredient_list = db.Column(db.Text,
                    nullable=False)
    recipe_notes = db.Column(db.Text,
                    nullable=True)
    cookbook_owner = db.Column(db.String(20),
                    db.ForeignKey("users.username", ondelete='cascade'),
                    nullable=False)
    