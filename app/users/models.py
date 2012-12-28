# third party imports
from sqlalchemy.sql import extract, func

# local application imports
from app import db
from app.users import constants as USER
from app.exercises.models import Exercise
from app.exercises.helpers import DateHelper


class User(db.Model):
	# Map model to db table
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), unique=True)
	email = db.Column(db.String(120), unique=True)
	password = db.Column(db.String(20))
	role = db.Column(db.SmallInteger, default=USER.USER)
	status = db.Column(db.SmallInteger, default=USER.NEW)
	exercises = db.relationship('Exercise', backref='user', lazy='dynamic')

	# Class Constructor
	def __init__(self, id=None):
		self.id = id

	# Factory Constructor of a new user to register
	@classmethod
	def NewUserToRegister(cls, name=None, email=None, password=None):
		_user = cls()
		_user.name = name
		_user.email = email
		_user.password = password
		return _user
	

	def getNameTitle(self):
		return self.name.title()

	def getStatus(self):
		return USER.STATUS[self.status]

	def getRole(self):
		return USER.ROLE[self.role]

	def getTotalExercises(self):
		return len(self.exercises.all())

	def getTotalExercisesCurrentWeek(self):

		start_end_week = DateHelper.get_start_end_days_current_week()
		start_week = start_end_week[0]
		end_week = start_end_week[1]

		return len(db.session.query(Exercise.id) 
						.filter(Exercise.user_id == self.id)
						.filter(Exercise.date >= start_week)
						.filter(Exercise.date <= end_week)
						.all())

	def getTotalExercisesCurrentMonth(self):
		current_month = DateHelper.current_month()

		return len(db.session.query(Exercise.id) 
						.filter(Exercise.user_id == self.id)
						.filter(extract('month', Exercise.date) == current_month)
						.all())


	def alreadyDidExerciseYesterday(self):

		yesterday = DateHelper.get_yesterday()

		return (len(db.session.query(Exercise.id) 
						.filter(Exercise.user_id == self.id)
						.filter(Exercise.date == yesterday)
						.all()) > 0)

	def __repr__():
		return '<User %r>' % (self.name)