from flask_project import db, uploaded_photos
from flask_wtf import Form, FlaskForm
from wtforms import validators, StringField, PasswordField, DateField, SelectField
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


# ApplicationForm is inheriting from the Form class
class ApplicationForm(FlaskForm):
    
    first_name = StringField('First Name', validators=[validators.Required(), validators.Length(min=1, max=80)])
    middle_name = StringField('Middle Name', validators=[validators.Optional(), validators.Length(min=1, max=80)])    
    last_name = StringField('Last Name', validators=[validators.Required(), validators.Length(min=1, max=80)])
    fathers_name = StringField('Fathers Name', validators=[validators.Required(), validators.Length(min=1, max=80)])
    
    date_of_birth = DateField('Date of Birth', [validators.Required()], format='%d/%m/%Y')
    place_of_birth = StringField('Place of Birth', validators=[validators.Required(), validators.Length(min=1, max=80)])
    

    pak_house_number = StringField('House/Unit number', validators=[validators.Required(), validators.Length(min=1, max=20)])
    pak_street = StringField('Street/Avenue/Road Name', validators=[validators.Required(), validators.Length(min=1, max=50)])
    pak_suburb = StringField('Suburb', validators=[validators.Required(), validators.Length(min=1, max=50)])
    pak_zipcode = StringField('Zip Code', validators=[validators.Required(), validators.Length(min=1, max=10)])
    pak_state = StringField('Province', validators=[validators.Required(), validators.Length(min=1, max=30)])

    aus_house_number = StringField('House/Unit number', validators=[validators.Required(), validators.Length(min=1, max=20)])
    aus_street = StringField('Street/Avenue/Road', validators=[validators.Required(), validators.Length(min=1, max=50)])
    aus_suburb = StringField('City/Suburb', validators=[validators.Required(), validators.Length(min=1, max=50)])
    aus_zipcode = StringField('Zip Code', validators=[validators.Required(), validators.Length(min=1, max=10)])
    aus_state = StringField('State', validators=[validators.Required(), validators.Length(min=1, max=30)])

    phone_number = StringField('Phone Number. Australia', validators=[validators.Required(), validators.Length(min=1, max=25)])
    email = EmailField('E-Mail Address', validators=[InputRequired('An email is required'), Email(), validators.Length(min=1, max=50)])
    
    pak_license_number = StringField('Pakistan Driving License No.', [validators.Optional(), validators.Length(min=8, max=30)])
    license_issuing_authority = StringField('License Issuing Authority', validators=[validators.Required(), validators.Length(min=1, max=80)])

    #license_category = StringField('License Category', [validators.Required()])
    
    pak_license_issue_date= DateField('License Issuing Date', format='%d/%m/%Y', validators=(RequiredIf('pak_license_number'),validators.Optional()))
    expiry_date_pakdl= DateField('Expiry Date - License', format='%d/%m/%Y', validators=(RequiredIf('pak_license_number'),validators.Optional()))
    
    aus_license_number = StringField('Australian Driving License No. (if any)', [validators.Optional(), validators.Length(min=8, max=25)])
    #expiry_date_ausdl= DateField('Expiry Date - License', format='%d/%M/%Y', validators=(RequiredIf('aus_license_number'),validators.Optional()))

    passport_number = StringField('Passport No.', [validators.Required(), validators.Length(min=1, max=29)])
    cnic_number = StringField('CNIC/NICOP No.', validators=[validators.Required(), validators.Length(min=1, max=30)])
  
    
class UploadForm(FlaskForm):
    
    current_photo = FileField('Current Photograph', validators=[FileRequired(),FileAllowed(uploaded_photos, 'Images only!')])
    current_dl = FileField('Current Drivers License', validators=[FileRequired(),FileAllowed(uploaded_photos, 'Images only!')])
    current_passport = FileField('Current Passport', validators=[FileRequired(),FileAllowed(uploaded_photos, 'Images only!')])
    current_noc = FileField('Current NOC (Optional)', validators=[FileAllowed(uploaded_photos, 'Images only!')])


class PaymentForm(FlaskForm):

    payment_type = SelectField(u'Payment Type', choices=[('Postal Money Order', 'Postal Money Order'), ('Certified Bank Cheque', 'Certified Bank Cheque'),
    ('Bank Draft', 'Bank Draft') , ('EFTPOS', 'EFTPOS'), ])


class ConfirmationForm(FlaskForm):
    confirmation_status = StringField('Confirmation')

class postalForm(FlaskForm):
    money_order_no = StringField('Money Order No.', validators=[validators.Required(), validators.Length(min=1, max=80)])
    date = DateField('Date', [validators.Required()], format='%d/%m/%Y')

class chequeForm(FlaskForm):
    issuing_bank_branch = StringField('Certifying Bank & Branch', validators=[validators.Required(), validators.Length(min=1, max=80)])
    bank_cheque_no = StringField('Certified Bank Cheque No.', validators=[validators.Required(), validators.Length(min=1, max=80)])
    date = DateField('Date', [validators.Required()], format='%d/%m/%Y')
    
class bankForm(FlaskForm):
    issuing_bank_branch = StringField('Issuing Bank & Branch', validators=[validators.Required(), validators.Length(min=1, max=80)])
    bank_order_no = StringField('Bank Draft Order No.', validators=[validators.Required(), validators.Length(min=1, max=80)])
    date = DateField('Date', [validators.Required()], format='%d/%m/%Y')
