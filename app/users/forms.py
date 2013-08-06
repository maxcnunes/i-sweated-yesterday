from flask.ext.wtf import Form, TextField, PasswordField, BooleanField
from flask.ext.wtf import Required, Email, EqualTo

class LoginForm(Form):
	email = TextField('Email address', [Required(), Email()])
	password = PasswordField('Password', [Required()])

class RecoverPasswordForm(Form):
	email = TextField('Email address', [Required(), Email()])

class RegisterForm(Form):
	name = TextField('NickName', [Required()])
	email = TextField('Email address', [Required()])
	receive_email_notification = BooleanField('Receive e-mail notifications')
	password = PasswordField('Password', [Required()])
	confirm = PasswordField('Repeat Password', [
		Required(),
		EqualTo('confirm', message='Passwords must match')
	])