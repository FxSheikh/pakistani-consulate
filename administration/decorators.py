from functools import wraps
from flask import session, request, redirect, url_for

def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		print("Testing")
		if session.get('admin') is False or session.get('admin') is None:
			return redirect(url_for('logout', next=request.url))
		return f(*args, **kwargs)
	return decorated_function