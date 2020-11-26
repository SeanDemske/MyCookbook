import os, requests, json
from flask import Flask, render_template, request, jsonify, redirect
from secrets import APP_ID, APP_KEY
from models import db, connect_db, User, Recipe

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql://postgres:developer@localhost:5432/mycookbook'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "secret")

# View functions
#----------------------------------------------------------------------

@app.route("/")
def homepage():
    """Show homepage"""

    return render_template("index.html")

@app.route("/ui")
def ui():
    """Route for testing UI"""

    return render_template("signup.html")

@app.route("/search")
def search_results():
    """Displays a list of search results"""

    search_query = request.args["q"]
    resp = requests.get(
        "https://api.edamam.com/search",
        params={
            "q": search_query,
            "app_id": APP_ID,
            "app_key": APP_KEY,
            "to": "30"
        }
    )

    results = resp.json().get("hits")
    return render_template("search_results.html", results=results, query=search_query)

@app.route("/recipes")
def api_recipe_detail():
    """Displays the details of a recipe"""

    search_query = request.args["r"]
    resp = requests.get(
        "https://api.edamam.com/search",
        params={
            "r": search_query,
            "app_id": APP_ID,
            "app_key": APP_KEY
        }
    )

    recipe = resp.json()[0]

    return render_template("api_recipe_detail.html", recipe=recipe)

# /search?q="chicken" GET

# /profile/<username> GET

# /profile/<username>/add GET/POST

# /recipes/<recipe_id> GET

# /recipes/<recipe_id>/add POST

# /signup GET/POST

# /signin GET/POST


