from flask import Flask, render_template, request, jsonify
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
                "app_id": "85ac62e0",
                "app_key": "6b7cae050360bfe22e3783935fba9187",
                "to": "20"
            }
        )
    
    results = resp.json()["hits"]

    return render_template("search_results.html", results=results)

@app.route("/ui")
def ui():
    """Testing UI"""

    return render_template("search_results.html")

# /search?q="chicken" GET

# /profile/<username> GET

# /profile/<username>/add GET/POST

# /recipes/<recipe_id> GET

# /recipes/<recipe_id>/add POST

# /signup GET/POST

# /signin GET/POST


