# third party imports
from sqlalchemy.sql import extract, func
import uuid

# local application imports
from app import db
from app.users import constants as USER
from app.exercises.models import Exercise
from app.exercises.helpers import DateHelper


class User(db.Model):
	# Map model to db table
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), unique=True)
	username = db.Column(db.String(50), unique=True)
	email = db.Column(db.String(120), unique=True)
	role = db.Column(db.SmallInteger, default=USER.USER)
	status = db.Column(db.SmallInteger, default=USER.NEW)
	email_exercise_token = db.Column(db.String(50))
	receive_email_notification = db.Column(db.Boolean(), default=False)
	oauth_key = db.Column(db.String(100))
	exercises = db.relationship('Exercise', backref='user', lazy='dynamic')

	# Class Constructor
	def __init__(self, id=None):
		self.id = id

	# @classmethod
	# def CreateUser(cls, name=None, email=None, receive_email_notification=None, oauth_key=None):
	# 	_user = cls()
	# 	_user.name = name
	# 	_user.email = email
	# 	_user.receive_email_notification = receive_email_notification
	# 	_user = oauth_key
	# 	return _user

	# Factory Constructor to create a user filled
	@classmethod
	def create_or_update_user_from_oauth(cls, name=None, username=None, email=None, password=None, oauth_key=None):
		is_new = False
		user = User.query.filter_by(email=email).first()
		if user is None:
			user = cls()
			is_new = True

		user.name = name
		user.username = username
		user.email = email
		user.password = password
		user.oauth_key = oauth_key

		if is_new:
			user.receive_email_notification = True
			db.session.add(user)
			
		db.session.commit()
		return user
	

	def get_picture(self):
		return 'http://graph.facebook.com/%s/picture' % self.username

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


	def alreadyDidExercise(self, date_exercise):

		return (len(db.session.query(Exercise.id) 
						.filter(Exercise.user_id == self.id)
						.filter(Exercise.date == date_exercise)
						.all()) > 0)

	
	def generate_key_recover_password(self):
		self.key_recover_password = str(uuid.uuid1())
		return self.key_recover_password

	def __repr__(self):
		return '<User %r>' % (self.name)