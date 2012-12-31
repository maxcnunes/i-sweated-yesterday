
from datetime import datetime, date, timedelta

class DateHelper(object):

	@staticmethod
	def get_yesterday():
		return (date.today() - timedelta(1))

	@staticmethod
	def current_month():
		return datetime.today().month

	@staticmethod
	def get_start_end_days_week(year, week):
		d = date(year,1,1)

		if(d.weekday()>3):
			d = d+timedelta(7-d.weekday())
		else:
			d = d - timedelta(d.weekday())
		dlt = timedelta(days = (week-1)*7)
		return d + dlt,  d + dlt + timedelta(days=6)


	@classmethod
	def get_start_end_days_current_week(cls):
		year = int(datetime.today().year)
		weeks_in_year = datetime.today()
		week = int(weeks_in_year.strftime("%W"))

		return cls.get_start_end_days_week(year, week)

	@staticmethod
	def datetime_to_string(value):
		"""Deserialize datetime object into string form for JSON processing."""

		if value is None:
			return None

		return [value.strftime("%d-%m-%Y"), value.strftime("%H:%M:%S")]

	@staticmethod
	def date_to_string(value):
		"""Deserialize date object into string form for JSON processing."""

		if value is None:
			return None

		return value.strftime("%d-%m-%Y")
		