from application import db
from sqlalchemy.orm import validates
import datetime

class User(db.Model):
	__tablename__ = 'User'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String, unique = True, nullable = False)
	password = db.Column(db.String, nullable = False)
	history = db.Column(db.String)
	entries = db.relationship('Entry', backref='user', lazy=True)

class Entry(db.Model):
	__tablename__ = 'Entry'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	userid = db.Column(db.Integer, db.ForeignKey('User.id'), nullable = False)
	failures = db.Column(db.Integer, nullable = False)
	is_math = db.Column(db.Integer, nullable = False)
	higher = db.Column(db.String, nullable = False)
	health = db.Column(db.Integer, nullable = False)
	Mjob = db.Column(db.String, nullable = False)
	studytime = db.Column(db.Integer, nullable = False)
	goout = db.Column(db.Integer, nullable = False)
	reason = db.Column(db.String, nullable = False)
	traveltime = db.Column(db.Integer, nullable = False)
	activities = db.Column(db.Integer, nullable = False)
	famsup = db.Column(db.String, nullable = False)
	nursery = db.Column(db.String, nullable = False)
	Total_alc = db.Column(db.Integer, nullable = False)
	prediction = db.Column(db.Float, nullable = False)
	predicted_on = db.Column(db.DateTime, nullable=False)
	children = db.relationship("Result", cascade="all,delete", backref='entry', lazy=True)

	@validates('id')
	def validate_id(self, key, id):
		if type(id) != int:
			raise Exception("ID must be int")
		if id <= 0:
			raise Exception("ID must be greater than 0")
		return id

	@validates('userid')
	def validate_userid(self, key, userid):
		if type(userid) != int:
			raise Exception("userid must be int")
		if userid <= 0:
			raise Exception("userid must be greater than 0")
		return userid

	@validates('is_math')
	def validate_is_math(self, key, is_math):
		if type(is_math) != int:
			try:
				is_math = int(is_math)
			except:
				raise Exception("is_math must be int")
		if not is_math in [0, 1]:
			raise Exception("is_math must be either 0 or 1")
		return is_math

	@validates('failures')
	def validate_failures(self, key, failures):
		if type(failures) != int:
			try:
				failures = int(failures)
			except:
				raise Exception("failures must be int")
		if failures < 0:
			raise Exception("failures cannot be negative")
		else:
			return int(failures)

	@validates('higher')
	def validate_higher(self, key, higher):
		if type(higher) != str:
			raise Exception("higher must be string")
		if not higher in ['yes', 'no']:
			raise Exception("higher must be one of ['yes', 'no']")

		return higher

	@validates('health')
	def validate_health(self, key, health):
		if type(health) != int:
			try:
				health = int(health)
			except:
				raise Exception("health must be an integer")
		if health < 1 or health > 5:
			raise Exception("health must be in between 1 and 5 inclusive")

		return int(health)

	@validates('Mjob')
	def validate_Mjob(self, key, Mjob):
		if type(Mjob) != str:
			raise Exception("Mjob must be a string")
		if not Mjob in ['teacher', 'health', 'services', 'at_home', 'other']:
			raise Exception("Mjob must be one of ['teacher', 'health', 'services', 'at_home', 'other']")
		return Mjob

	@validates('studytime')
	def validate_studytime(self, key, studytime):
		if type(studytime) != int:
			try:
				studytime = int(studytime)
			except:
				raise Exception("studytime must be an integer")
		if studytime < 0:
			raise Exception("studytime cannot be negative")
		return int(studytime)

	@validates('goout')
	def validate_goout(self, key, goout):
		if type(goout) != int:
			try:
				goout = int(goout)
			except:
				raise Exception("goout must be an integer")
		if goout < 1 or goout > 5:
			raise Exception("goout must be in between 1 and 5 inclusive")
		return int(goout)

	@validates('reason')
	def validate_reason(self, key, reason):
		if type(reason) != str:
			raise Exception("reason must be a string")
		if not reason in ['home', 'reputation', 'course', 'other']:
			raise Exception("reason must be one of ['home', 'reputation', 'course', 'other']")
		return reason

	@validates('traveltime')
	def validate_traveltime(self, key, traveltime):
		if type(traveltime) != int:
			try:
				traveltime = int(traveltime)
			except:
				raise Exception("traveltime must be an integer")
		if traveltime < 0:
			raise Exception("traveltime cannot be negative")
		return int(traveltime)

	@validates('activities')
	def validate_activities(self, key, activities):
		if type(activities) != str:
			raise Exception("activities must be a string")
		if not activities in ['yes', 'no']:
			raise Exception("activities must be one of ['yes', 'no']")
		return activities

	@validates('famsup')
	def validate_famsup(self, key, famsup):
		if type(famsup) != str:
			raise Exception("famsup must be a string")
		if not famsup in ['yes', 'no']:
			raise Exception("famsup must be one of ['yes', 'no']")
		return famsup 

	@validates('nursery')
	def validate_nursery(self, key, nursery):
		if type(nursery) != str:
			raise Exception("nursery must be a string")
		if not nursery in ['yes', 'no']:
			raise Exception("nursery must be one of ['yes', 'no']")
		return nursery 

	@validates('Total_alc')
	def validate_Total_alc(self, key, Total_alc):
		if type(Total_alc) != int:
			try:
				Total_alc = int(Total_alc)
			except:
				raise Exception("Total_alc must be an integer")
		if Total_alc < 0 or Total_alc > 5:
			raise Exception("Total_alc must be in between 1 and 5 inclusive")
		return int(Total_alc)

	@validates('prediction')
	def validate_prediction(self, key, prediction):
		if type(prediction) != float:
			try:
				prediction = float(prediction)
			except:
				raise Exception("prediction must be a float")
		if prediction < 0 or prediction > 4:
			raise Exception("Total_alc must be in between 0 and 4 inclusive")
		return float(prediction)

	@validates('predicted_on')
	def validate_predicted_on(self, key, predicted_on):
		if type(predicted_on) != type(datetime.datetime.now()):
			raise Exception("prediction must be a datetime")
		else:
			return predicted_on

	def as_dict(self, include_columns):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name in include_columns}

class Result(db.Model):
	__tablename__ = 'Result'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	entryid = db.Column(db.Integer, db.ForeignKey('Entry.id', ondelete='CASCADE'), nullable = False)
	improve_image_path = db.Column(db.String)
	improve_title = db.Column(db.String)
	improve_text = db.Column(db.String)
	good_image_path = db.Column(db.String)
	good_title = db.Column(db.String)
	good_text = db.Column(db.String)
	public_can_view = db.Column(db.Boolean)

	@validates('improve_image_path')
	def validate_improve_image_path(self, key, improve_image_path):
		if type(improve_image_path) != str:
			raise Exception("improve_image_path must be a string")
		elif not improve_image_path.count('.') == 1:
			raise Exception("improve_image_path must be a file")
		else:
			return improve_image_path

	@validates('improve_title')
	def validate_improve_title(self, key, improve_title):
		if type(improve_title) != str:
			raise Exception("improve_title must be a string")
		else:
			return improve_title

	@validates('improve_text')
	def validate_improve_text(self, key, improve_text):
		if type(improve_text) != str:
			raise Exception("improve_text must be a string")
		else:
			return improve_text


	@validates('good_image_path')
	def validate_good_image_path(self, key, good_image_path):
		if type(good_image_path) != str:
			raise Exception("good_image_path must be a string")
		elif not good_image_path.count('.') == 1:
			raise Exception("good_image_path must be a file")
		else:
			return good_image_path

	@validates('good_title')
	def validate_good_title(self, key, good_title):
		if type(good_title) != str:
			raise Exception("good_title must be a string")
		else:
			return good_title

	@validates('good_text')
	def validate_good_text(self, key, good_text):
		if type(good_text) != str:
			raise Exception("good_text must be a string")
		else:
			return good_text
