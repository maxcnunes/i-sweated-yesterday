from flask import Flask, render_template, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail

app = Flask(__name__)
app.config.from_object('settings')

db = SQLAlchemy(app)

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