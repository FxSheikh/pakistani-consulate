from functools import wraps
from flask import session, request, redirect, url_for, flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('useremail') is None:
        	flash("Insufficient rights, please log in.")
        	return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

