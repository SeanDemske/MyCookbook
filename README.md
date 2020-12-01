## MyCookbook

<p>
    A mobile responsive website for finding and keeping track of new recipes
    <br />
    <a href="https://myonlinecookbook.herokuapp.com/">View Live</a>
</p>

![Website](https://i.imgur.com/5N1sMIB.png)

## Description

I was inspired to create this project from my recent interest in cooking. I wanted to create something that I myself would find practical and useful. I wanted an easy way for people to find new ideas for things to make and also a place to keep track of all their recipes.
* Find and discover new recipes to impress the whole family. No account needed
* Sign up for an account and you'll be able to store your favorite recipes that you find
* From your account you can modify the recipes and add additional notes in case you decide you want to tweak anything

## Built With
* Python
* Javascript
* HTML
* CSS
* [Jinja](https://jinja.palletsprojects.com/en/2.11.x/)
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [Postgres](https://www.postgresql.org/)
* [SQL Alchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
* [Flask-Bcrypt](https://flask-bcrypt.readthedocs.io/en/latest/)
* [WTForms](https://wtforms.readthedocs.io/en/2.3.x/)
* [Font Awesome](https://fontawesome.com/)
* [Edamam Recipe API](https://developer.edamam.com/edamam-docs-recipe-api )


## Setting up the developer environment on Windows:
1.) Install Python 3.7.9  
2.) Install PostgreSQL  
3.) Open a new terminal and cd into the root directory  
4.) Create your virtual environment with Python (type "python -m venv venv")  
5.) Activate your environment (". venv/Scripts/activate")  
6.) Install the dependencies with pip "pip install -r requirements.txt"  
7.) Create your database "createdb mycookbook" with a password of "developer"  
8.) Initialize the tables by running "python seed.py" in the terminal  
9.) Register for an API key at https://developer.edamam.com/edamam-docs-recipe-api (free)  
10.) Find and replace "APP_ID_GOES_HERE" and "APP_KEY_GOES_HERE" with your credentials  
11.) Run the application with "flask run"  


## Roadmap
Due to deadlines I wasn't able to include all the functionality I would have liked. Features I'd like to implement at a later date include:
* Allow users to create their own recipes
* Advanced search filters
* Sharing your cookbook with other users
* Page functionality for recipe searches
