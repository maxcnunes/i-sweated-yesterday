# third party imports
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from werkzeug import check_password_hash, generate_password_hash
from datetime import datetime
from sqlalchemy.sql import or_

# local application imports
from app import db
from app.users.forms import RegisterForm, LoginForm
from app.users.models import User
from app.users.requests import app_before_request
from app.users.decorators import requires_login
from app.users.constants import SESSION_NAME_USER_ID
from app.exercises.models import Exercise


mod = Blueprint('users', __name__, url_prefix='/users')


@mod.before_request
def before_request():
	app_before_request()


@mod.route('/')
@mod.route('/me/')
@requires_login
def index():
	return render_template('users/profile.html', user=g.user)


@mod.route('/login/', methods=['GET', 'POST'])
def login():
	form = LoginForm(request.form)
	# make sure data are valid, but doesn't validate password is right
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		# we use werzeug to validate user's password
		if user and check_password_hash(user.password, form.password.data):
			# the session can't be modified as it's signed,
			# it's a safe place to store the user id
			session[SESSION_NAME_USER_ID] = user.id
			flash('Welcome %s' % user.name)
			return redirect(url_for('users.index'))
		flash('Wrong email or password', 'error-message')
	return render_template( 'users/login.html', form=form)


@mod.route('/register/', methods=['GET', 'POST'])
def register():
	form = RegisterForm(request.form)

	if form.validate_on_submit():

		userRegistered = User.query.filter(or_(User.name == form.name.data,\
												User.email == form.email.data)).first()
		if userRegistered is not None:
			flash('Email or user already is registered')
			return render_template('users/register.html', form=form)

		# create an user instance not yet stored in the database
		user = User.NewUserToRegister(form.name.data, form.email.data,\
						generate_password_hash(form.password.data))

		# insert the record in our database and commit it
		db.session.add(user)
		db.session.commit()

		# log the user in, as he now has an id
		session[SESSION_NAME_USER_ID] = user.id

		# flash will display a message to the user
		flash('Thanks for registering')

		# redirect user to the 'index' method of the user module
		return redirect(url_for('users.index'))
	return render_template('users/register.html', form=form)


@mod.route('/logout/', methods=['GET'])
def logout():
	# remove the username from the session if it's there
	session.pop(SESSION_NAME_USER_ID, None)

	# flash will display a message to the user
	flash('Do not forget keep the exercises')

	# redirect user to the 'index' method of the user module
	return redirect(url_for('users.login'))

