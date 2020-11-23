from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


# View functions
#----------------------------------------------------------------------

@app.route("/")
def homepage():
    """Show homepage"""

    return render_template("index.html")