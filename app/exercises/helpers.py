
from datetime import datetime, date, timedelta

class DateHelper(object):

	@staticmethod
	def get_current_date():
		return datetime.today()

	@staticmethod
	def get_yesterday():
		return (date.today() - timedelta(1))

	@staticmethod
	def current_month():
		return datetime.today().month

	@staticmethod
	def current_year():
		return datetime.today().year

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
	def get_week_in_year(value):
		return int(value.strftime("%W"))


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

	@staticmethod
	def date_to_year_month_string(value):
		"""Deserialize date object into year month string form for JSON processing."""

		if value is None:
			return None

		return value.strftime("%m-%Y")
		

	@staticmethod
	def generate_id_by_month_year(value) :

		if value is None:
			return None

		return int(value.strftime("%m") + value.strftime("%Y"))

	@staticmethod
	def generated_id_by_month_year_to_date(value):

		if value is None:
			return None

		month = int(str(value)[:2])
		year = int(str(value)[2:])

		return date(year,month,1)