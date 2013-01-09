# third party imports
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, abort
from sqlalchemy.sql import func, extract, desc

# local application imports
from app import db
from app.exercises.forms import IDidExerciseForm, TotalOnWeekByMonthForm, ExercisesByMonthForm
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
	form = IDidExerciseForm(request.form)
	return render_template('exercises/i_did.html', form=form)


@mod.route('/i_did', methods=['POST'])
@requires_login
def idid():
	form = IDidExerciseForm(request.form)

	# get the exercise date
	if(form.date_exercise_type.data == 'yesterday'):
		date_exercise = DateHelper.get_yesterday()
	else:
		date_exercise = DateHelper.string_to_date(form.date_exercise.data)

	if date_exercise > DateHelper.get_current_date().date():
		flash('Exercise date can not be newer than today')
		return render_template('exercises/i_did.html', form=form)

	if g.user.alreadyDidExercise(date_exercise):
		flash('You already did exercise on this date: %s' % date_exercise)
		return render_template('exercises/i_did.html', form=form)
	
	# create a new object to exercise
	exercise = Exercise(date_exercise, g.user.id)

	# insert the record in our db and commit it
	db.session.add(exercise)
	db.session.commit()

	# display a message to the user
	flash('Keep fitness and do it again tomorrow')

	# redirect user to the 'index' method of the user module
	return redirect(url_for('users.index'))

@mod.route('/general/')
def general():
	# get the total of exercises every user have done since the begin
	results = db.session.query(User.name, func.count(User.name).label('total'))\
						.group_by(User.name)\
						.filter(Exercise.user_id == User.id)\
						.all()

	# convert list to dictonary
	data = {name: str(total) for (name, total) in results}

	return render_template('exercises/general.html', data=data)


@mod.route('/total_on_week_by_month/', methods=['GET','POST'])
@requires_login
def total_on_week_by_month():
	# get all months a user have done exercises
	all_months = db.session.query(Exercise.date)\
						.group_by(extract('year', Exercise.date), extract('month', Exercise.date), Exercise.date)\
						.order_by(desc(Exercise.date))\
						.filter(Exercise.user_id == g.user.id)\
						.all()

	form = TotalOnWeekByMonthForm(request.form)
	# set all months as options of SELECT element on the form
	form.months.choices = [(DateHelper.generate_id_by_month_year(item.date), 
							DateHelper.date_to_year_month_string(item.date)) 
							for item in all_months]

	# when is a POST action
	if form.validate_on_submit():
		date_selected = DateHelper.generated_id_by_month_year_to_date(form.months.data)

		# get the total exercises a user have done per week on a selected month
		results = db.session.query(func.strftime('%W', Exercise.date).label('week'), func.count(Exercise.date).label('total'))\
						.group_by(func.strftime('%W', Exercise.date))\
						.filter(extract('month', Exercise.date) == date_selected.month)\
						.filter(extract('year', Exercise.date) == date_selected.year)\
						.filter(Exercise.user_id == g.user.id)\
						.all()

		# convert list to dictonary
		data = {('Week %s on year' % (week)): str(total) for (week, total) in results}

		return render_template('exercises/total_on_week_by_month.html', form=form, data=data)
	return render_template('exercises/total_on_week_by_month.html', form=form)


@mod.route('/exercises_by_month/', methods=['GET','POST'])
@requires_login
def exercises_by_month():

	# get all months a user have done exercises
	all_months = db.session.query(Exercise.date)\
						.group_by(extract('year', Exercise.date), extract('month', Exercise.date), Exercise.date)\
						.order_by(desc(Exercise.date))\
						.filter(Exercise.user_id == g.user.id)\
						.all()

	form = ExercisesByMonthForm(request.form)
	# set all months as options of SELECT element on the form
	form.months.choices = [(DateHelper.generate_id_by_month_year(item.date), 
							DateHelper.date_to_year_month_string(item.date)) 
							for item in all_months]

	#
	# GET
	#
	if request.method == 'GET':
		return render_template('exercises/exercises_by_month.html', form=form)

	#
	# POST
	#
	if request.form["action"] == "Search":
		exercises = get_exercises_by_month(form.months.data)

	elif request.form["action"] == "Delete":
		if not request.form.getlist('do_delete'):
			exercises = get_exercises_by_month(form.months.data)
			flash('Select least one exercise to delete')
		else:
			for id_exercise in request.form.getlist('do_delete'):
				# get exercise by id
				exercise = Exercise.query.get(int(id_exercise))
				# delete
				db.session.delete(exercise)
			
			# commit
			db.session.commit()

			flash('Exercise(s) was(were) deleted successfully', 'success')
			return redirect(url_for('users.index'))

	return render_template('exercises/exercises_by_month.html', exercises=exercises, form=form)


@mod.route("/mark_exercise_by_email/<email_token>", methods=['GET'])
def mark_exercise_by_email(email_token):

	date_exercise = DateHelper.get_yesterday()

	user = User.query.filter_by(email_exercise_token=email_token).first()

	if(user is None):
		flash('Operation not allowed')
		return abort(404)

	if user.alreadyDidExercise(date_exercise):
		flash('You already did exercise on this date: %s' % date_exercise)
		return redirect(url_for('index'))

	# create a new object to exercise
	exercise = Exercise(date_exercise, user.id)

	# insert the record in our db and commit it
	db.session.add(exercise)
	db.session.commit()

	# display a message to the user
	flash('Keep fitness and do it again tomorrow')

	return redirect(url_for('index'))


def get_exercises_by_month(date_search):
	date_selected = DateHelper.generated_id_by_month_year_to_date(date_search)

	exercises = db.session.query(Exercise)\
		.filter(
			Exercise.user_id == g.user.id,\
			extract('month', Exercise.date) == date_selected.month,\
		).all()

	return exercises
