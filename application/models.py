from flask_project import db, uploaded_photos
import datetime

# Creating a model for applications
class Application(db.Model):
    id = db.Column(db.String(13), primary_key=True, default=None)
    applicant_id = db.Column(db.Integer, db.ForeignKey('applicant.id'))

    first_name = db.Column(db.String(80))
    middle_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))

    fathers_name = db.Column(db.String(80))
    
    date_of_birth = db.Column(db.Date)
    place_of_birth = db.Column(db.String(80))
    
    aus_house_number = db.Column(db.String(20))
    aus_street = db.Column(db.String(50))
    aus_suburb = db.Column(db.String(50))
    aus_zipcode = db.Column(db.String(10))
    aus_state = db.Column(db.String(30))

    pak_house_number = db.Column(db.String(20))
    pak_street = db.Column(db.String(50))
    pak_suburb = db.Column(db.String(50))
    pak_zipcode = db.Column(db.String(10))
    pak_state = db.Column(db.String(30))
    
    pak_license_number = db.Column(db.String(40))
    expiry_date_pakdl = db.Column(db.Date)
    pak_license_issue_date = db.Column(db.Date)
    
    license_issuing_authority = db.Column(db.String(80))
    
    aus_license_number = db.Column(db.String(30))
    
    passport_number = db.Column(db.String(30))
    
    cnic_number = db.Column(db.String(30))

    phone_number = db.Column(db.String(25))
    email = db.Column(db.String(35))

    remarks = db.Column(db.String(255))


    
    # current_photo = db.Column(db.String(255))
    # driving_license_copy = db.Column(db.String(255))
    # passport_copy = db.Column(db.String(255))
    # noc_pakistan_copy = db.Column(db.String(255))
    
    pending_status = db.Column(db.String(255), default="Pending")
    status_change = db.Column(db.String(5), default="False")
    date_submitted = db.Column(db.DateTime)
    
    current_photo = db.Column(db.String(255), default=None)
    driving_license = db.Column(db.String(255), default=None)
    passport_copy = db.Column(db.String(255), default=None)
    noc_pakistan = db.Column(db.String(255), default=None)
    payment_type = db.Column(db.String(255), default=None)

    issuing_bank_branch = db.Column(db.String(80), default=None)
    bank_cheque_no = db.Column(db.String(80), default=None)

    bank_order_no = db.Column(db.String(80), default=None)

    card_type = db.Column(db.String(80), default=None)
    card_no = db.Column(db.String(80), default=None)
    receipt_no = db.Column(db.String(80), default=None)

    money_order_no = db.Column(db.String(80), default=None)
    amount = db.Column(db.String(10), default=None)
    date = db.Column(db.Date)

    
    
    def __init__(self, applicant_id, form, unique_id, curr_date):
        self.id = unique_id
        self.applicant_id = applicant_id

        self.first_name = form.first_name.data
        self.middle_name = form.middle_name.data
        self.last_name = form.last_name.data
        self.fathers_name = form.fathers_name.data

        self.date_of_birth = form.date_of_birth.data
        self.place_of_birth = form.place_of_birth.data

        self.aus_house_number = form.aus_house_number.data
        self.aus_street = form.aus_street.data
        self.aus_suburb = form.aus_suburb.data
        self.aus_zipcode = form.aus_zipcode.data
        self.aus_state = form.aus_state.data

        self.pak_house_number = form.pak_house_number.data
        self.pak_street = form.pak_street.data
        self.pak_suburb = form.pak_suburb.data
        self.pak_zipcode = form.pak_zipcode.data
        self.pak_state = form.pak_state.data

        #self.australian_address = "{0} {1} {2} {3} {4}".format(form.aus_house_number.data, form.aus_street.data, form.aus_suburb.data, form.aus_zipcode.data, form.aus_state.data)
        #self.pakistan_address = "{0} {1} {2} {3} {4}".format(form.pak_house_number.data, form.pak_street.data, form.pak_suburb.data, form.pak_zipcode.data, form.pak_state.data)

        self.pak_license_number = form.pak_license_number.data
        self.expiry_date_pakdl = form.expiry_date_pakdl.data
        self.pak_license_issue_date = form.pak_license_issue_date.data
        self.license_issuing_authority = form.license_issuing_authority.data
        self.aus_license_number = form.aus_license_number.data
        #self.expiry_date_ausdl = form.expiry_date_ausdl.data
        self.passport_number = form.passport_number.data
        #self.expiry_date_passport = form.expiry_date_passport.data
        self.cnic_number = form.cnic_number.data
        #self.expiry_date_cnic = form.expiry_date_cnic.data
        self.pending_status = "Saved"
        self.email = form.email.data
        self.phone_number = form.phone_number.data
        self.date_submitted = curr_date

    @property
    def current_photo_src(self):
        return uploaded_photos.url(self.current_photo)

    

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<Application %r>' % self.applicant_id
    


        
        
 