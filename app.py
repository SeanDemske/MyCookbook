import os, requests, json
from flask import Flask, render_template, request, jsonify, redirect, session, g
from models import db, connect_db, User, Recipe
from forms import RegisterForm, LoginForm, RecipeEditForm
from utilities import password_confirmed
from sqlalchemy.exc import IntegrityError

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql://postgres:developer@localhost:5432/mycookbook'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "secret")

connect_db(app)

@app.before_request
def add_user_to_g():
    """If we have our stamp to get in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.username


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
        g.user = None

# View functions
#----------------------------------------------------------------------

@app.route("/")
def homepage():
    """Show homepage"""

    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def user_register_form():
    """Handles user registration"""

    register_form = RegisterForm()
    
    if register_form.validate_on_submit():
        try:
            if password_confirmed(register_form.password.data, register_form.password_confirm.data):
                user = User.register(
                    username=register_form.username.data,
                    email=register_form.email.data,
                    password=register_form.password.data
                )
                db.session.commit()
                do_login(user)
            else:
                print("passwords don't match") # FLAGGED
        except IntegrityError:
            print ("Error") # FLAGGED

        return redirect("/")
    else:
        return render_template("signin_signup.html", form=register_form)

@app.route("/login", methods=["POST", "GET"])
def user_login_form():
    """Display login page"""

    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.authenticate(login_form.username.data, login_form.password.data)
        print(user)
        if user:
            do_login(user)
            return redirect("/")

    return render_template("signin_signup.html", form=login_form)

@app.route("/logout")
def logout():
    """Signs out the current user"""

    do_logout()
    return redirect("/")

@app.route("/search")
def search_results():
    """Displays a list of search results"""

    search_query = request.args["q"]
    resp = requests.get(
        "https://api.edamam.com/search",
        params={
            "q": search_query,
            "app_id": os.environ.get('APP_ID', APP_ID),
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
            "app_id": os.environ.get('APP_ID', APP_ID),
            "app_key": APP_KEY
        }
    )

    recipe = resp.json()[0]

    return render_template("api_recipe_detail.html", recipe=recipe)


# User
#----------------------------------------------------------------------

@app.route("/<username>/cookbook")
def cookbook_profile(username):
    """Route to take the user to their profile/cookbook"""

    if not g.user:
        return redirect("/login")

    saved_recipes = g.user.recipes

    return render_template("user/cookbook.html", recipes=saved_recipes)

@app.route("/<username>/delete", methods=["POST"])
def delete_profile(username):

    if not g.user:
        return redirect("/login")

    if not g.user.username == username:
        return redirect("/")

    db.session.delete(g.user)
    db.session.commit()
    do_logout()

    return redirect("/")


@app.route("/<username>/cookbook/save", methods=["POST", "GET"])
def save_recipe(username):

    if not g.user:
        return redirect("/login")

    search_query = request.args["r"]
    resp = requests.get(
        "https://api.edamam.com/search",
        params={
            "r": search_query,
            "app_id": os.environ.get('APP_ID', APP_ID),
            "app_key": APP_KEY
        }
    )

    try:
        recipe_json = resp.json()[0]
        recipe_object = g.user.add_recipe(recipe_json, g.user.username)
        db.session.add(recipe_object)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return redirect(f"/{g.user.username}/cookbook")

    
    return redirect(f"/{g.user.username}/cookbook")

@app.route("/<username>/cookbook/<recipe_name>")
def view_cookbook_recipe(username, recipe_name):

    if not g.user:
        return redirect("/login")

    recipe = g.user.recipes.filter_by(title=recipe_name).first()

    return render_template("user/cookbook_recipe_detail.html", recipe=recipe)

@app.route("/<username>/cookbook/<recipe_name>/delete", methods=["POST"])
def delete_cookbook_recipe(username, recipe_name):

    if not g.user:
        return redirect("/login")

    recipe = g.user.recipes.filter_by(title=recipe_name).first()

    db.session.delete(recipe)
    db.session.commit()

    return redirect(f"/{username}/cookbook")
    
@app.route("/<username>/cookbook/<recipe_name>/edit", methods=["POST", "GET"])
def edit_cookbook_recipe(username, recipe_name):

    if not g.user:
        return redirect("/login")

    recipe = g.user.recipes.filter_by(title=recipe_name).first()
       
    edit_form = RecipeEditForm()

    if edit_form.validate_on_submit():
        try:
            recipe.title = edit_form.title.data
            recipe.recipe_image_url = edit_form.recipe_image.data
            recipe.recipe_notes = edit_form.additional_notes.data
            print(recipe.title)
            db.session.add(recipe)
            db.session.commit()
        except IntegrityError:
            print ("Error") # FLAGGED

        return redirect(f"/{username}/cookbook/{recipe.title}")
    else:
        edit_form.title.data = recipe.title
        edit_form.recipe_image.data = recipe.recipe_image_url
        edit_form.additional_notes.data = recipe.recipe_notes
        return render_template("user/edit_recipe_form.html", form=edit_form, recipe=recipe)