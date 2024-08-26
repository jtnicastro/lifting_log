from app import db, login_manager
from flask_login import UserMixin

class User(UserMixin, db.Model):
	user_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(30))
	email = db.Column(db.String(50))
	password = db.Column(db.String(50))

	# Method required by Flask-Login to return the unique identifier for the user
	def get_id(self):
		return (self.user_id)

class Workout(db.Model):
	workout_id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
	workout_name = db.Column(db.String(50))

	# Establishes a one-to-many relationship with Exercises
	exercises = db.relationship('Exercises', backref='workout', lazy='dynamic')

class Exercises(db.Model):
	exercise_id = db.Column(db.Integer, primary_key=True)
	workout_id = db.Column(db.Integer, db.ForeignKey('workout.workout_id'))
	exercise_name = db.Column(db.String(50))

class Workout_log(db.Model):
	log_id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
	workout_id = db.Column(db.Integer, db.ForeignKey('workout.workout_id'))
	log_date = db.Column(db.DateTime)

	workout = db.relationship('Workout', backref='logs')
	log_details = db.relationship('Log_details', backref='workout_log', lazy='dynamic')

class Log_details(db.Model):
	detail_id = db.Column(db.Integer, primary_key=True)
	log_id = db.Column(db.Integer, db.ForeignKey('workout_log.log_id'))
	exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.exercise_id'))
	sets = db.Column(db.Integer)
	weight = db.Column(db.Integer)
	repetitions = db.Column(db.Integer)

	exercise = db.relationship('Exercises')

# This callback is used by Flask-Login to reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))