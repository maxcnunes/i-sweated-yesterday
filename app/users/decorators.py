from functools import wraps
from flask import g, flash, redirect, url_for, request
from threading import Thread

def requires_login(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if g.user is None:
			flash(u'You need to be signed in for this page.')
			return redirect(url_for('users.login', next=request.path))
		return f(*args, **kwargs)
	return decorated_function


def redirect_to_profile_logged_users(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		# verify if the user is already logged
		if g.user is not None:
			flash(u'You are already logged. To access that page do the logout before.')
			return redirect(url_for('users.index'))
		return f(*args, **kwargs)
	return decorated_function


def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper