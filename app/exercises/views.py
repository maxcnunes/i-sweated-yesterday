from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

from app import db
from app.exercises.forms import ExerciseForm
from app.exercises.models import Exercise
from app.exercises.helpers import DateHelper
from app.users.constants import SESSION_NAME_USER_ID
from app.users.models import User


mod = Blueprint('exercises', __name__, url_prefix='/exercises')

@mod.route('/')
@mod.route('/i_did', methods=['GET'])
def index():
	return render_template('exercises/i_did.html')


@mod.route('/i_did', methods=['POST'])
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
