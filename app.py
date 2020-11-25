from flask import Flask, render_template, request, jsonify, redirect
from secrets import APP_ID, APP_KEY
import requests
import json

app = Flask(__name__)

# View functions
#----------------------------------------------------------------------

@app.route("/")
def homepage():
    """Show homepage"""

    return render_template("index.html")

@app.route("/browse")
def browse():
    """Testing displayed collection"""

    resp = requests.get(
            "https://api.edamam.com/search",
            params={
                "q": "chicken",
                "app_id": APP_ID,
                "app_key": APP_KEY,
                "to": "20"
            }
        )
    
    results = resp.json()["hits"]

    return render_template("search_results.html", results=results)

@app.route("/ui")
def ui():
    """Testing UI"""

    return render_template("search_results.html")

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
            "to": "20"
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


