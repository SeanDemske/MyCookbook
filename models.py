"""Models for User and Recipes"""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

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

    @classmethod
    def register(cls, username, email, password):
        """Creates a new user and adds it to the database. Returns user instance"""

        hashed_password = bcrypt.generate_password_hash(password).decode("UTF-8")
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)

        return user
    
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
    