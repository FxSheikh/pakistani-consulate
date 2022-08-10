from flask_project import app
from flask_project import administration
from flask import render_template, redirect, flash, url_for, session, request
import configparser


@app.route('/index')
def index():
	if 'useremail' in session:
		# flash("user %s logged in" % session['useremail'])
		return redirect(url_for('login_success'))
	else:
	    return redirect(url_for('login'))