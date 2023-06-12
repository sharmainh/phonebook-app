# Forms is a helper file that allows us to ensure that users are giving us the right data. For example: if someone is entering an email address on the application, we do need to check to make sure it is a valid email address.

# This file will import special tools that will help us make sure that users are giving us the right information. Weve used concepts like Regex before. We could write our own Regex OR have someone write it for us and then import their module. Thats what were going to do below, on the next line, import regex. 
# There are other modules we imported here as well that help us handle our data

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class UserLoginForm(FlaskForm): # This is what were pulling from routes.py
    email = StringField('Email', validators = [DataRequired(), Email()]) # This line here is our email variable, that makes sure it is a string input and we make sure users give it that data (DataRequired()), AND make sure its an email format(Email())
    password = PasswordField('Password', validators = [DataRequired()])  # Were going to do the same thing for password, wtforms will keep your password safe by converting the password to little dots when the user enters password, and prevent users from being able to see your password.
    submit_button = SubmitField() # There is submit button code in a different file forms.html