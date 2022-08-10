from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_project import setup
from flask_admin import Admin

# creating an instance of the Flask app
app = Flask(__name__)

# setting the configuration of the application from a settings file
app.config.from_object('setup')

# db holds the database
db = SQLAlchemy(app)

#admin setup
admin = Admin(app, name='microblog', template_mode='bootstrap3')

#mail
mail = Mail(app)

# migrations 
migrate = Migrate(app, db)

# uploadset configuration
uploaded_photos = UploadSet('photos', ('jpg', 'jpe', 'jpeg', 'png', 'pdf'))
uploaded_licenses = UploadSet('licenses', ('jpg', 'jpe', 'jpeg', 'png', 'pdf'))
uploaded_passports = UploadSet('passports', ('jpg', 'jpe', 'jpeg', 'png', 'pdf'))
uploaded_nocs = UploadSet('nocs', ('jpg', 'jpe', 'jpeg', 'png', 'pdf'))


configure_uploads(app, (uploaded_photos, uploaded_licenses, uploaded_passports, uploaded_nocs))

# importing all of the views from the various modules
from home import views
from applicant import views
from application import views
from administration import views

