from flask_project import app, db
from flask import render_template, redirect, flash, url_for, session, request, send_file, send_from_directory
from applicant.models import Applicant
from administration.form import CGStatusForm, COStatusForm, CAStatusForm, AdminForm
from administration.decorators import login_required
from application.models import Application
from sqlalchemy.exc import IntegrityError
import configparser, bcrypt, csv, datetime
import os


@app.route('/view_applications')
@login_required
def view_applications():
		status_list = {}
		status_list['submitted'] = Application.query.filter_by(pending_status="Submitted").count()
		status_list['rejected'] = Application.query.filter_by(pending_status="Rejected").count()

		status_list['received'] = Application.query.filter_by(pending_status="Received").count()
		status_list['returned'] = Application.query.filter_by(pending_status="Returned").count()
		status_list['recc_approval'] = Application.query.filter_by(pending_status="Recommended For Approval").count()
		status_list['recc_rejection'] = Application.query.filter_by(pending_status="Recommended For Rejection").count()
		status_list['recc_3rd'] = Application.query.filter_by(pending_status="Recommended For 3rd Party").count()

		
		sqlQuery = "SELECT * from application WHERE pending_status != 'Archived'"
		appList = db.session.execute(sqlQuery)

		return render_template('administration/admin_dashboard.html', status_list=status_list, user=session['admin_type'], appList=appList)

def assert_access(status):
	admin_level = session['admin_type']
	if admin_level == "CG":
		return True
	if status == "Saved":
		if admin_level == 'CG':
			return True
	elif status == "Submitted":
			return True
	elif status == "Received":
		if admin_level == "CA":
			return True
	elif status == "Returned":
		return True
	elif status == "Recommended For Approval":
		if admin_level == "CO":
			return True
	elif status == "Recommended For Rejection":
		if admin_level == "CO":
			return True
	elif status == "Recommended For 3rd Party":
		if admin_level == "CO":
			return True
	elif status == "Referred For 3rd Party":
		if admin_level == "CO":
			return True
	elif status == "Approved":
		if admin_level == "CO":
			return True
	elif status == "Rejected":
		if admin_level == "CO":
			return True
	elif status == "view_applicants":
		if admin_level == "CO":
			return True

	return False

def assert_modify(status):
	admin_level = session['admin_type']
	if admin_level == "CG":
		return True
	if status == "Saved":
		if admin_level == 'CG':
			return True
	elif status == "Submitted":
			return True
	elif status == "Received":
		if admin_level == "CA":
			return True
	elif status == "Returned":
		if admin_level == 'CG':
			return True
	elif status == "Recommended For Approval":
		if admin_level == "CO":
			return True
	elif status == "Recommended For Rejection":
		if admin_level == "CO":
			return True
	elif status == "Recommended For 3rd Party":
		if admin_level == "CO":
			return True
	elif status == "Referred For 3rd Party":
		if admin_level == "CO":
			return True
	elif status == "Approved":
		if admin_level == "CO":
			return True
	elif status == "Rejected":
		if admin_level == "CO":
			return True
	elif status == "view_applicants":
		if admin_level == "CO":
			return True

	return False



@app.route('/view_dl_applications/<string:status>')
@login_required
def view_dl_applications(status):
	if assert_access(status): 
		if (status == "All"):
			sqlQuery = "SELECT * from application ORDER BY date_submitted ASC"
		else:
			sqlQuery = "SELECT * from application WHERE pending_status = '{0}' ORDER BY date_submitted ASC".format(status)
		appList = db.session.execute(sqlQuery)
	else:
		flash("Insufficient access rights to this application status.")
		return redirect(url_for('view_applications'))
	return render_template('administration/application_list.html', appList=appList, status=status)


@app.route('/view_applicants')
@login_required
def view_applicants():
	if assert_access("view_applicants"): 
		sqlQuery = "SELECT * from applicant"
		applicantList = db.session.execute(sqlQuery)
	else:
		flash("Insufficient access rights to this application status.")
		return redirect(url_for('view_applications'))
	return render_template('administration/applicant_list.html', applicantList=applicantList)

@app.route('/delete_applicant/<string:applicant_id>', methods=('GET','POST'))
@login_required
def delete_applicant(applicant_id):	
	try:
		Applicant.query.filter_by(id=applicant_id).delete()
		flash("Applicant {0} deleted".format(applicant_id))
		db.session.commit()
		db.session.flush()
	except:
		flash("Could not delete. Application attached to user.")
	return redirect(url_for('view_applicants'))



@app.route('/delete_application/<string:applicant_id>', methods=('GET','POST'))
@login_required
def delete_application(applicant_id):	
	try:
		if session['admin_type'] == 'CG':
			Application.query.filter_by(id=applicant_id).delete()
			flash("Application {0} deleted".format(applicant_id))
			db.session.commit()
			db.session.flush()
		else:
			flash("Insufficient rights.")
	except:
		flash("Could not delete. ")
	return redirect(url_for('view_dl_applications', status="All"))


@app.route('/get_app/<string:application_id>', methods=('GET','POST'))
@login_required
def get_app(application_id):
	application = Application.query.filter_by(id=application_id).first()	
	remarks = db.session.query(Application.remarks).filter_by(id=application_id).first()	

	if session['admin_type'] == 'CG':
		form = CGStatusForm(obj=remarks)
	elif session['admin_type'] == 'CO':
		form = COStatusForm(obj=remarks)
	else:
		form = CAStatusForm(obj=remarks)

	sqlQuery = "SELECT * FROM application WHERE application.id = '{0}'".format(application_id)
	applicant = db.session.execute(sqlQuery)
	return render_template('administration/current_application.html', applicant=applicant, form=form)


@app.route('/change_status/<string:application_id>', methods=('GET','POST'))
@login_required
def change_status(application_id):
	application = Application.query.filter_by(id=application_id).first()

	if session['admin_type'] == 'CG':
		form = CGStatusForm()
	elif session['admin_type'] == 'CO':
		form = COStatusForm()
	else:
		form = CAStatusForm()
	if assert_access(application.pending_status) and assert_modify(application.pending_status):
		if form.validate_on_submit:
			if form.pending_status.data == "Disabled" or form.pending_status.data == "None":
				flash("You did not choose an application status.")
				return redirect(url_for('get_app', application_id=application_id))
			#Ensure process flow from submitted to received
			print("Debug: ", form.pending_status.data)
			if application.pending_status == 'Submitted' and form.pending_status.data != "Received":
				flash("You have insufficient rights to change this status from " + application.pending_status +" to "+ form.pending_status.data)
				return redirect(url_for('get_app', application_id=application_id))
			print(application.pending_status)
			application.pending_status = form.pending_status.data
			application.status_change = "True"
			application.remarks = form.remarks.data
			db.session.commit()
			db.session.flush()
			flash("Changed status for application to " + form.pending_status.data)
			flash("Remark set")

			if form.pending_status.data == "Approved" and assert_access(form.pending_status.data):
				flash("Changed status for application to " + form.pending_status.data)
				return redirect(url_for('show_acceptance_letter', application_id=application.id))
			elif form.pending_status.data == "Rejected" and assert_access(form.pending_status.data):
				flash("Changed status for application to " + form.pending_status.data)
				return redirect(url_for('show_rejection_letter', application_id=application.id))		
			
	else:
		flash("You have insufficient rights to change this status")
	return redirect(url_for('get_app', application_id=application_id))


@app.route('/generate_acceptance/<string:application_id>', methods=('GET','POST'))
@login_required
def generate_acceptance(application_id):
	# msg = Message(
 #              'Your Acceptance Letter - Pakistani Consulate Sydney',
	#        sender='alinaeem2006@gmail.com',
	#        recipients=
 #               ['alinaeem2006@gmail.com'])
	# msg.body = "This is the email body"
	# msg.html = "<strong>Testing how good</strong> HTML is for sending <br> emails"
	# mail.send(msg)
	# flash("Acceptance letter sent")
	return redirect(url_for('show_acceptance_letter', application_id=application_id))

@app.route('/generate_rejection/<string:application_id>', methods=('GET','POST'))
@login_required
def generate_rejection(application_id):
	# msg = Message(
 #              'Your Rejection Letter - Pakistani Consulate Sydney',
	#        sender='alinaeem2006@gmail.com',
	#        recipients=
 #               ['alinaeem2006@gmail.com'])
	# msg.body = "This is the email body"
	# msg.html = "<strong>Testing how good</strong> HTML is for sending <br> emails"
	# mail.send(msg)
	# flash("Rejection letter sent")
	return redirect(url_for('show_rejection_letter', application_id=application_id))


@app.route('/show_acceptance_letter/<string:application_id>')
@login_required
def show_acceptance_letter(application_id):
	application = Application.query.filter_by(id=application_id).first()
	applicant = Applicant.query.filter_by(email=session['useremail']).first()
	curr_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	return render_template('letters/acceptance.html', app=application, date=curr_date, user=applicant)

@app.route('/show_rejection_letter/<string:application_id>')
@login_required
def show_rejection_letter(application_id):
	application = Application.query.filter_by(id=application_id).first()
	curr_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	return render_template('letters/rejection.html', app=application, date=curr_date)

@app.route('/download_applications/<string:status>')
def download_applications(status):
	destination = os.path.join(app.config['UPLOADED_APPLIST_DEST']) + "/applist_{0}.csv".format(status)
	application_list = open(destination, 'w')
	outcsv = csv.writer(application_list)
	records = None
	if (status == "All"):
		records = db.session.query(Application)
	else:	
		records = db.session.query(Application).filter_by(pending_status=status)

	cursor = db.session.execute(records)
	
	columns = db.session.execute(records).keys()

	outcsv.writerow(x for x in columns)
	outcsv.writerows(cursor.fetchall())

	
	application_list.close()
	return send_file(os.path.join(app.config['UPLOADED_APPLIST_DEST']) + "/applist_{0}.csv".format(status), attachment_filename='applist.csv', as_attachment=True)



@app.route('/add_administrator', methods=('GET', 'POST'))
def add_administrator():
	form = AdminForm()
	if form.validate_on_submit():
		salt = bcrypt.gensalt()
		hashed_password = bcrypt.hashpw(form.password.data, salt)
		
		try:
			applicant = Applicant(form.first_name.data, form.middle_name.data,
			form.last_name.data, form.phone_number.data, form.email.data, hashed_password, True, form.admin_type.data)
			db.session.add(applicant)
			db.session.flush()
			
			if applicant.id:
				db.session.commit()
				flash("Administrator registered")            
				return redirect(url_for('view_applications'))
			else:
				db.session.rollback();
				error = "Error registering applicant"
			
		except IntegrityError: 
			flash("This email already exists in our system.")
			emailerror = "This email already exists in our system."
			return render_template('administration/add_admin.html', form=form, error=error, emailerror=emailerror)
			
	return render_template('administration/add_admin.html', form=form)