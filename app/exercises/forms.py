from flask.ext.wtf import Form, TextField
from flask.ext.wtf import Required

class ExerciseForm(Form):
	description = TextField('Description')
	