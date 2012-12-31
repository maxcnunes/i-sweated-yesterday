# third party imports
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, json, jsonify
from sqlalchemy.sql import func

# local application imports
from app import db
from app.exercises.forms import ExerciseForm
from app.exercises.models import Exercise
from app.exercises.helpers import DateHelper
from app.users.constants import SESSION_NAME_USER_ID
from app.users.models import User
from app.users.requests import app_before_request
from app.users.decorators import requires_login


mod = Blueprint('exercises', __name__, url_prefix='/exercises')


@mod.before_request
def before_request():
	app_before_request()


@mod.route('/')
@mod.route('/i_did', methods=['GET'])
@requires_login
def index():
	return render_template('exercises/i_did.html')


@mod.route('/i_did', methods=['POST'])
@requires_login
def idid():
	# get the date of yesterday and the current user id
	yesterday = DateHelper.get_yesterday()
	user_id = session[SESSION_NAME_USER_ID]
	
	# create a new object to exercise
	exercise = Exercise(yesterday, user_id)

	user = User(user_id)
	if user.alreadyDidExerciseYesterday():
		flash('You already did exercise yesterday')
		return render_template('exercises/i_did.html')

	# insert the record in our db and commit it
	db.session.add(exercise)
	db.session.commit()

	# display a message to the user
	flash('Keep fitness and do it again tomorrow')

	# redirect user to the 'index' method of the user module
	return redirect(url_for('users.index'))

@mod.route('/general/')
def general():
	results = db.session.query(User.name, func.count(User.name).label('total'))\
						.group_by(User.name)\
						.filter(Exercise.user_id == User.id)\
						.all()


	# convert to dictonary
	data = {name: str(total) for (name, total) in results}

	return render_template('exercises/general.html', data=data)
