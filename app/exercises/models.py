from app import db

class Exercise(db.Model):
	# Map model to db table
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.Date())
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __init__(self, date=None, user_id=None):
		self.date = date
		self.user_id = user_id

	def __repr__(self):
		return '<Exercise %r>' % (self.id)


