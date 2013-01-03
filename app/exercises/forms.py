from flask.ext.wtf import Form, Required, RadioField, HiddenField, SelectField, DateField
from app.exercises.helpers import DateHelper

class IDidExerciseForm(Form):
	date_exercise_type = RadioField('When',
								validators=[Required()],
								choices=[('yesterday', 'Yesterday'), ('another_day', 'Another day')],
								default='yesterday')

	date_exercise = HiddenField(default=DateHelper.date_to_string(DateHelper.get_yesterday()), 
								id='date_exercise')

class TotalOnWeekByMonthForm(Form):
	months = SelectField(u'Months', coerce=int)

class ExercisesByMonthForm(Form):
	months = SelectField(u'Months', coerce=int)
	