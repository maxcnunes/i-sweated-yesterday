from flask.ext.mail import Message
from threading import Thread
import uuid

from app import mail_sender
from app.users.decorators import async
from app import db
from app.exercises.helpers import DateHelper
from app.users.models import User
from app.exercises.models import Exercise



def send_email_to_users_have_forgotten_add_last_exercise():
	reset_exercise_token_all_users()

	url_app = u'http://maxcnunes.pythonanywhere.com/'
	
	for user in get_all_users_want_receive_mail_notification():
		user.email_exercise_token = str(uuid.uuid1())

		url_confirmation = '%sexercises/mark_exercise_by_email/%s' % (url_app, user.email_exercise_token)

		msg =	'<h2>Did you sweat yesterday?</h2>'\
			 	'You have no marked yet a exercise for yesterday.<br/>'\
				'If you forgot, please just submit '\
				'<a href="' + url_confirmation + '">here</a> to automatically mark a exercise for yesterday.<br/>'\
				'Or access the I sweated yesterday - Application '\
				'<a href="' + url_app + '">here</a>'

		send_async_email('I sweated yesterday - Notification', user.email, msg)

	
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

	

