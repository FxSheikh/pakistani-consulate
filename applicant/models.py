from flask_project import db

# Creating a model for the applicant or the external users of the system
class Applicant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    middle_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    phone_number = db.Column(db.String(10))
    email = db.Column(db.String(35), unique=True)
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean())
    admin_type = db.Column(db.String(80))

    def __init__(self, first_name, middle_name, last_name, phone_number, email, password, admin, admin_type):
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = email
        self.password = password
        self.admin = admin
        self.admin_type = admin_type

    def __str__(self):
        return self.email
        
    def __repr__(self):
        return '<Applicant %r>' % self.email

# We need to ask Sir, if a username is required, or is email sufficient
# We need to ak Sir, if NOC upload is required
# We need to ask Sir, what maximum upload size is for a single upload document
# We need to ask Sir, about the format of the serial number (letters, numbers, or combination)