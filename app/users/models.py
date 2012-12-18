from app import db
from app.users import constants as USER
from app.exercises.models import Exercise

from sqlalchemy.sql import extract, func
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
		"""
		current_year = datetime.today().year
		current_month = datetime.today().month

		weeks_in_year = datetime.today()
		current_week = int(weeks_in_year.strftime("%W"))

		query = db.session.query(Exercise)\
						.filter(Exercise.user_id == self.id)\
						.filter(extract('year', Exercise.date) == current_year)\
						.filter(extract('month', Exercise.date) == current_month)\
						.all()
		
		count = 0
		for item in query:
			if int(item.date.strftime("%W")) == current_week :
				count += 1

		return count
		
		return len(db.session.query(Exercise.id) 
						.filter(Exercise.user_id == self.id)
						.filter(extract('year', Exercise.date) == current_year)
						.filter(func.strftime('%w', Exercise.date) == current_week)
						#.filter(int(Exercise.date.strftime("%W")) == current_week)
						.all())
		#return self.query.filter(User.id == 1).first().id
		"""

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