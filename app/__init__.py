import os
from flask import Flask, render_template, session
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail
from flask_oauth import OAuth


app = Flask(__name__)
app.config.from_object('settings')


# Authentication Facebook
oauth = OAuth()
FACEBOOK_APP_ID = os.environ['ISY_FACEBOOK_APP_ID']
FACEBOOK_APP_SECRET = os.environ['ISY_FACEBOOK_APP_SECRET']
facebook = oauth.remote_app('facebook',
  base_url='https://graph.facebook.com/',
  request_token_url=None,
  access_token_url='/oauth/access_token',
  authorize_url='https://www.facebook.com/dialog/oauth',
  consumer_key=FACEBOOK_APP_ID,
  consumer_secret=FACEBOOK_APP_SECRET,
  request_token_params={'scope': 'email'}
)

# Database
db = SQLAlchemy(app)

# Mailer
mail_sender = Mail(app)

# Basic Routes #

@app.route('/')
def index():
	return render_template('main/index.html')

@app.errorhandler(404)
def not_found(error):
	return render_template('404.html'), 404


# BluePrints - Modules #

# Users Module
from app.users.views import mod as usersModule
app.register_blueprint(usersModule)

# Exercises Module
from app.exercises.views import mod as exercisesModule
app.register_blueprint(exercisesModule)