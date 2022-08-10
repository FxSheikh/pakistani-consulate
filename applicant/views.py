from flask_project import app
from flask_project import administration
from flask_project import db
from flask import render_template, redirect, flash, url_for, session, request
from applicant.models import Applicant
from applicant.form import LoginForm
from applicant.form import RegisterForm
from applicant.decorators import login_required
from sqlalchemy.exc import IntegrityError
import configparser
import bcrypt
import pymysql

@app.errorhandler(404)
def page_not_found(e):
    return redirect('index')

# this route will test the database connection and nothing more
# @app.route('/')
# def testdb():
#     # try:
#     #     db.session.query("1").from_statement("SELECT 1").all()
#     #     return '<h1>It works.</h1>'
#     # except:
#     #     return '<h1>Something is broken.</h1>'

#     db.create_all()
#     db.session.commit()
#     guest = Applicant("Theo", "-", "James", "0412345678", "guest@mail.com", 'password', False, "")
#     db.session.add(guest)
#     db.session.commit()
    
#     first_user = Applicant.query.filter_by(email='guest@mail.com').first()
#     if not first_user:
#         return 'No result found'
#     else:
#         return first_user.email 


@app.route('/create_admin')
def create_admin():
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw("admin12345678", salt)
    applicant = Applicant("Administrator", "-", "-", "0411484361", "cg@consulate.com", hashed_password, True, "CG")
    db.session.add(applicant)
    db.session.flush()
    db.session.commit()
    return redirect(url_for('login'))


@app.route('/register', methods=('GET','POST'))
def register():
    form = RegisterForm()
    error = None
    if 'useremail' in session:
        return redirect('index')
    if form.validate_on_submit():
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(form.password.data, salt)
        
        try:
            applicant = Applicant(form.first_name.data, form.middle_name.data, form.last_name.data, form.phone_number.data, form.email.data, hashed_password, None, None)
            db.session.add(applicant)
            db.session.flush()
            
            if applicant.id:
                db.session.commit()
                flash("Applicant registered")            
                return redirect(url_for('login'))
            else:
                db.session.rollback();
                error = "Error registering applicant"
            
        except IntegrityError: 
            flash("This email already exists in our system.")
            emailerror = "This email already exists in our system."
            return render_template('applicant/register.html', form=form, error=error, emailerror=emailerror)
            
    return render_template('applicant/register.html', form=form, error=error)


@app.route('/login', methods=('GET','POST'))    
def login():
    session.pop('useremail', None)
    session.pop('firstname', None)
    session.pop('admin', None)
    session.pop('application_id', None)
    form = LoginForm()
    error = None

    if request.method == 'GET' and request.args.get('next'):
        session['next'] = request.args.get('next', None)
        
    if form.validate_on_submit():
        user_email = Applicant.query.filter_by(email=form.email.data,).first()
        
        if user_email:
            if bcrypt.hashpw(form.password.data, user_email.password) == user_email.password:
                session['useremail'] = form.email.data
                session['firstname'] = user_email.first_name
                if user_email.admin:
                    session['admin'] = True
                    user = Applicant.query.filter_by(email=session['useremail']).with_entities(Applicant.admin_type).first()
                    session['admin_type'] = user[0]
                    print("Set admin type as ", session['admin_type'])
                else:
                    session['admin'] = False
                flash("Welcome %s." % session['firstname'])
                if 'next' in session:
                    next = session.get('next')
                    session.pop('next', None)
                    return redirect(next)
                else:
                    if session['admin']:
                        return redirect(url_for('view_applications'))
                    else:
                        return redirect(url_for('login_success'))
            else:
                error = "Incorrect username and password"
        else:
            error = "Incorrect username and password"
    return render_template('applicant/login.html', form=form, error=error)


@app.route('/logout')
def logout():
    if session.get('firstname'):
        flash("Goodbye, %s." % session['firstname'])
    session.pop('useremail', None)
    session.pop('firstname', None)
    session.pop('admin', None)
    session.pop('application_id', None)
    return redirect(url_for('login'))    
    
    
@app.route('/login_success')
@login_required
def login_success():
    if session['admin'] is True:
        return redirect('view_applications')
    else:
        return render_template('index/index.html') 
    

# https://stackoverflow.com/questions/24522290/cannot-catch-sqlalchemy-integrityerror
# https://stackoverflow.com/questions/11313935/trying-to-catch-integrity-error-with-sqlalchemy    