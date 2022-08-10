from flask_wtf import Form, FlaskForm
from wtforms import validators, StringField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, InputRequired

#RegisterForm is inheriting from the Form class
class RegisterForm(FlaskForm):
    first_name = StringField('First Name', [validators.Required()])
    middle_name = StringField('Middle Name')    
    last_name = StringField('Last Name', [validators.Required()])
    phone_number = StringField('Phone Number', [validators.Required(), validators.Length(min=8, max=10)])
    email = EmailField('Email', [validators.Required(),Email()])
    password = PasswordField('Password', [validators.Required(),
            validators.EqualTo('password_confirm', message='Passwords must match'),validators.Length(min=4, max=80)])
    password_confirm = PasswordField('Repeat Password', [validators.Required()])


#LoginForm is inheriting from the Form class
class LoginForm(FlaskForm):
    email = EmailField('Enter your email', validators=[InputRequired('An email is required'), Email(), validators.Length(min=3, max=50)])
    password = PasswordField('Enter your password', validators=[InputRequired('A password is required'), validators.Length(min=4, max=80)]) 
