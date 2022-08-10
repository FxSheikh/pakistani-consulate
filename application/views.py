from flask_project import app
from flask_project import db
from flask_project import uploaded_photos, uploaded_licenses, uploaded_passports, uploaded_nocs
from flask import render_template, redirect, flash, url_for, session, request, send_from_directory
from application.models import Application
from application.form import ApplicationForm, UploadForm, PaymentForm, ConfirmationForm, postalForm, bankForm, chequeForm
from applicant.models import Applicant
from application.decorators import login_required
import configparser, bcrypt, string, random, datetime
from werkzeug import secure_filename
import os

@app.errorhandler(413)
def request_entity_too_large(error):
    flash("Entity too large")
    return redirect(url_for('upload'))

def update_application(application, form, unique_id, curr_date):
        application.id = unique_id
        application.first_name = form.first_name.data
        application.middle_name = form.middle_name.data
        application.last_name = form.last_name.data
        application.fathers_name = form.fathers_name.data

        application.date_of_birth = form.date_of_birth.data
        application.place_of_birth = form.place_of_birth.data

        application.aus_house_number = form.aus_house_number.data
        application.aus_street = form.aus_street.data
        application.aus_suburb = form.aus_suburb.data
        application.aus_zipcode = form.aus_zipcode.data
        application.aus_state = form.aus_state.data


        application.pak_house_number = form.pak_house_number.data
        application.pak_street = form.pak_street.data
        application.pak_suburb = form.pak_suburb.data
        application.pak_zipcode = form.pak_zipcode.data
        application.pak_state = form.pak_state.data


        application.pak_license_number = form.pak_license_number.data
        application.expiry_date_pakdl = form.expiry_date_pakdl.data

        application.pak_license_issue_date = form.pak_license_issue_date.data
        application.license_issuing_authority = form.license_issuing_authority.data

        application.aus_license_number = form.aus_license_number.data
        application.passport_number = form.passport_number.data
        application.cnic_number = form.cnic_number.data
        application.pending_status = "Saved"
        application.email = form.email.data
        application.phone_number = form.phone_number.data
        application.date_submitted = curr_date
        db.session.commit()
        db.session.flush()
        return True

@app.route('/static/documents/<path:filename>')
def protected(filename):
    # application = Application.query(Application.current_photo,
    # Application.driving_license, Application.passport_copy, Application.noc_pakistan).filter_by(id=session['application_id']).first()
    if session['admin'] is False:
        flash("Insufficient privilleges to view file.")
        return redirect(url_for('index'))

    return send_from_directory('static/documents', filename)


@app.route('/dl_information')
@login_required
def dl_information():
    return render_template('application/dl_instructions.html')

#Initial application route, generates form and commits response to database
@app.route('/dl_application', methods=('GET','POST'))
@login_required
def dl_application():
    #Create a unique ID for application if there already isn't an existent one from an ongoing application
    new_application = False
    if session.get('application_id') is None:
        session['application_id'] = id_generator()
        print("id generated")
        new_application = True
    application = Application.query.filter_by(id=session['application_id']).first()
    
    if application is None:
        form = ApplicationForm()
        new_application = True
    else:
        form = ApplicationForm(obj=application)
    
    error = None
    # if there is a session implying a user is logged in then we do the following:
    applicant = Applicant.query.filter_by(email=session['useremail']).first()
    print(new_application)
    if form.validate_on_submit():
        if new_application is True:
            curr_date = datetime.datetime.now()
            application = Application(applicant.id, form, session['application_id'], curr_date)
            print("Date of birth:", form.date_of_birth.data, form.pak_license_issue_date.data, form.expiry_date_pakdl.data)
            db.session.add(application)
            #db.session.flush()
            db.session.commit()
            db.session.flush()
            flash("Application created")
            return redirect(url_for('upload', application_id=application.id))   
        else:
            curr_date = datetime.datetime.now()
            update_application(application, form, session['application_id'], curr_date)
            return redirect(url_for('upload', application_id=application.id))   

    return render_template('application/dlv_application.html', form=form, error=error) 



@app.route('/upload', methods=('GET','POST'))
@login_required
def upload():
    application_id = session.get('application_id')
    application = Application.query.filter_by(id=application_id).first()
    form = UploadForm(obj=application)
    if session.get('application_id') is None:
        return redirect(url_for('dl_application'))

    if form.validate_on_submit():
        
        current_photo_filename = None
        current_license_filename = None
        current_passport_filename = None
        current_noc_filename = None
        try:
            current_photo_filename = uploaded_photos.save(request.files.get('current_photo'))
        except:
            flash("Current photograph was not uploaded")
            
        try:
            current_license_filename = uploaded_licenses.save(request.files.get('current_dl'))
        except:
            flash("License document was not uploaded")            

        try:
            current_passport_filename = uploaded_passports.save(request.files.get('current_passport'))
        except:
            flash("Passport document was not uploaded")

        try:
            current_noc_filename = uploaded_nocs.save(request.files.get('current_noc'))
        except:
            flash("NOC was not uploaded")


        application.current_photo = current_photo_filename
        application.driving_license = current_license_filename
        application.passport_copy = current_passport_filename
        application.noc_pakistan = current_noc_filename
        flash("Files uploaded")
        db.session.commit()
        db.session.flush()

        return redirect(url_for('payment_details'))
        
    return render_template('application/dlv_upload.html', form=form, application_id=application_id, application=application)  
    

@app.route('/payment_details', methods=('GET','POST'))
def payment_details():
    application = Application.query.filter_by(id=session['application_id']).first()
    form = PaymentForm()
    if form.validate_on_submit():
        application.payment_type = form.payment_type.data
        db.session.commit()
        db.session.flush()
        return redirect(url_for('enter_payment'))
    return render_template('application/payment_details.html', form=form)

@app.route('/enter_payment', methods=('GET', 'POST'))
def enter_payment():
    if session.get('application_id') is None:
        return redirect(url_for('dl_application'))
    application = Application.query.filter_by(id=session['application_id']).first()

    payment_method = application.payment_type
    if payment_method == "Postal Money Order":
        form = postalForm(obj=application)
    elif payment_method == "Certified Bank Cheque":
        form = chequeForm(obj=application)
    elif payment_method == "Bank Draft":
        form = bankForm(obj=application)
    elif payment_method == "EFTPOS":
        application.payment_type = "EFTPOS"
        db.session.commit()
        db.session.flush()
        flash("All credit and debit cards are acceptable at the Consulate General counter. You may print and present your application, along with copies of your document to deposit processing fee during consular hours.")
        return redirect(url_for('confirm_details'))

    if form.validate_on_submit():
        flash("Payment details stored.")
        if payment_method == "Postal Money Order":
            application.payment_type = "Postal Money Order"
            application.money_order_no = form.money_order_no.data
            application.date = form.date.data
            db.session.commit()
            db.session.flush()
        elif payment_method == "Certified Bank Cheque":
            application.payment_type = "Certified Bank Cheque"
            application.issuing_bank_branch = form.issuing_bank_branch.data
            application.bank_cheque_no = form.bank_cheque_no.data
            application.date = form.date.data
        elif payment_method == "Bank Draft":
            application.payment_type = "Bank Draft"
            application.issuing_bank_branch = form.issuing_bank_branch.data
            application.bank_order_no = form.bank_order_no.data
            application.date = form.date.data
        elif payment_method == "EFTPOS":
            application.card_type = form.card_type.data
            application.card_no = form.card_no.data
            application.receipt_no = form.receipt_no.data
            application.date = form.date.data
        db.session.commit()
        db.session.flush()
        return redirect(url_for('confirm_details'))

    return render_template('application/enter_payment.html', form=form, payment_method=payment_method)

@app.route('/confirm_details')
def confirm_details():
    form = ConfirmationForm()
    application = Application.query.filter_by(id=session['application_id']).first()
    if form.validate_on_submit():
        return redirect(url_for('submit_application'))
    return render_template('application/dlv_confirmation.html', x=application)

@app.route('/submit_application')
def submit_application():
    if session.get('application_id') is None:
        return redirect(url_for('dl_application'))

    unique_id = session.get('application_id')
    application = Application.query.filter_by(id=unique_id).first()
    application.pending_status = "Submitted"
    db.session.commit()
    db.session.flush()
    session.pop('application_id', None)
    return render_template('application/dlv_successful.html', serial_num=unique_id, x=application)
    
# secure and clear function for generating a unique application serial number
def id_generator(size=12, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(size))  

@app.route('/user_applications')
def user_applications():
    applicant = Applicant.query.filter_by(email=session['useremail']).first()
    sqlQuery = "SELECT * FROM application WHERE application.applicant_id = " + str(applicant.id)
    applicant = db.session.execute(sqlQuery)
    return render_template('application/view_applications.html', applicant=applicant)    
    
  
# https://ikpdb.readthedocs.io/en/1.0.x/index.html
# https://c9.io/blog/debugging-python-on-cloud9/
