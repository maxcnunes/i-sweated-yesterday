from flask.ext.wtf import Form, SelectField

class TotalOnWeekByMonthForm(Form):
	months = SelectField(u'Months', coerce=int)
	