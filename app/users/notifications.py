from flask.ext.mail import Message
from threading import Thread
import uuid
import logging

import app
from app import mail_sender
from app.users.decorators import async
from app import db
from app.exercises.helpers import DateHelper
from app.users.models import User
from app.exercises.models import Exercise

# Config Log
logging.basicConfig(
	filename='log_notifications.log',
	level=logging.INFO,
	format='%(asctime)s %(message)s', 
	datefmt='%m/%d/%Y %I:%M:%S %p'
)


def send_email_to_users_have_forgotten_add_last_exercise():
	logging.info('\n')
	logging.info('Start send e-mails notificatios')

	reset_exercise_token_all_users()
	logging.info('Reseted token e-mails of all users')

	url_app = u'http://isweatedyesterday.herokuapp.com/'
	
	users_to_send_notifications = get_all_users_want_receive_mail_notification()
	logging.info('Amount of users to send notification: %02d', len(users_to_send_notifications))

	for user in users_to_send_notifications:
		user.email_exercise_token = str(uuid.uuid1())

		url_confirmation = '%sexercises/mark_exercise_by_email/%s' % (url_app, user.email_exercise_token)

		msg =	'<h2>Did you sweat yesterday?</h2>'\
			 	'You have not marked yet a exercise for yesterday.<br/>'\
				'If you forgot, please just submit '\
				'<a href="' + url_confirmation + '">here</a> to automatically mark a exercise for yesterday.<br/>'\
				'Or access the I sweated yesterday - Application '\
				'<a href="' + url_app + '">here</a>'

		send_async_email('I sweated yesterday - Notification', user.email, msg)
		logging.info('Notification sent to %s', user.name)

	
	db.session.commit()
	logging.info('Commit changes in to database')

	logging.info('End send e-mails notificatios')


def send_email_to_recover_user_password(user_email):
	user = User.query.filter_by(email=user_email).first()
	user.generate_key_recover_password()

	url_app = u'http://isweatedyesterday.herokuapp.com/'
	url_confirmation = '%susers/recover_password_key/%s' % (url_app, user.key_recover_password)

	msg =	'<h2>Password Recovery</h2>'\
			'To recover your password click '\
			'<a href="' + url_confirmation + '">here</a>'

	send_async_email('I sweated yesterday - Password Recovery', user.email, msg)
	
	db.session.commit()


def get_all_users_want_receive_mail_notification():
	yesterday = DateHelper.get_yesterday()

	# get all users want to receive email notification
	# and didn't do exercise yesterday
	users = db.session.query(User)\
						.filter(User.receive_email_notification)\
						.filter(User.exercises.any(Exercise.date == yesterday) == False)\
						.all()
	return users

def reset_exercise_token_all_users():
	# get all users
	users = db.session.query(User).all()

	# reset exercise token of all users
	for user in users:
		user.email_exercise_token = ''

	db.session.commit()

@async
def send_async_email(subject, to, text_html):

	msg = Message(
			subject,
			sender='you@google.com',
			recipients=[to],
			html=text_html)

	#msg.html = msg

	mail_sender.send(msg)

	

