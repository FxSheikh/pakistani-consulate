from flask_project import db, uploaded_photos
from flask_wtf import Form, FlaskForm
from wtforms import validators, StringField, PasswordField, DateField, TextField, SelectField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, InputRequired, ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired
# from wtforms.fields.html5 import DateField


class RequiredIf(InputRequired):
    # a validator which makes a field required if another field is set and has a truthy value

    def __init__(self, other_field_name, *args, **kwargs):
        self.other_field_name = other_field_name
        super(RequiredIf, self).__init__(*args, **kwargs)

    def __call__(self, form, field):
        other_field = form._fields.get(self.other_field_name)
        if other_field is None:
            raise Exception('no field named "%s" in form' % self.other_field_name)
        if bool(other_field.data):
            super(RequiredIf, self).__call__(form, field)
  
class CGStatusForm(FlaskForm):
    remarks = TextAreaField('Remarks', validators=[validators.Required()])
    pending_status = SelectField(u'Application Status', choices=[('disabled', 'Choose an option'), ('Saved', 'Saved'), ('Submitted', 'Submitted'),
    ('Returned', 'Returned'),  ('Approved', 'Approved'),
    ('Rejected', 'Rejected'), ('Received', 'Received'), ('Archived', 'Archived'), ('Recommended For Approval', 'Recommended For Approval'),
    ('Recommended For Rejection', 'Recommended For Rejection'), ('Recommended for 3rd Party', 'Recommended for 3rd Party'),
    ('Referred for 3rd Party', 'Referred for 3rd Party')]
    )
  
class CAStatusForm(FlaskForm):
    remarks = TextAreaField('Remarks', validators=[validators.Required()])
    pending_status = SelectField(u'Application Status', choices=[('disabled', 'Choose an option'), ('Received', 'Received'), ('Recommended For Approval', 'Recommended For Approval'),
    ('Recommended For Rejection', 'Recommended For Rejection'), ('Recommended for 3rd Party', 'Recommended for 3rd Party'), ('Returned', 'Returned')]
    )
  
class COStatusForm(FlaskForm):
    remarks = TextAreaField('Remarks', validators=[validators.Required()])
    pending_status = SelectField(u'Application Status', choices=[('disabled', 'Choose an option'), ('Approved', 'Approved'), ('Referred For 3rd Party', 'Referred For 3rd Party'),
    ('Rejected', 'Rejected'), ('Returned', 'Returned')])
  
  
class AdminForm(FlaskForm):
    first_name = StringField('First Name', [validators.Required()])
    middle_name = StringField('Middle Name')    
    last_name = StringField('Last Name', [validators.Required()])
    phone_number = StringField('Phone Number', [validators.Required(), validators.Length(min=8, max=10)])
    email = EmailField('Email', [validators.Required(),Email()])
    password = PasswordField('Password', [validators.Required(),
            validators.EqualTo('password_confirm', message='Passwords must match'),validators.Length(min=4, max=80)])
    password_confirm = PasswordField('Repeat Password', [validators.Required()])
    admin_type = SelectField(u'Administrational Role', choices=[('CG', 'Consul General'), ('CO', 'Consular Officer'),
    ('CA', 'Consular Assistant') , ])
