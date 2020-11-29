from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

class RegisterForm(FlaskForm):
    """Username Email Password"""

    form_title = "Register"
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("EMail", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[Length(min=6)])
    password_confirm = PasswordField("Confirm Password", validators=[Length(min=6)])

class LoginForm(FlaskForm):
    """Username Password"""

    form_title = "Login"
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])