from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, BooleanField, IntegerField, FieldList, FormField
from wtforms.validators import InputRequired, Length 

class RegisterForm(FlaskForm):
	username = StringField('Username', validators=[InputRequired('A username is required.'), Length(max=30, message='Username can\'t exceed 30 characters.')])
	email = EmailField('Email', validators=[InputRequired('An email is required')])
	password = PasswordField('Password', validators=[InputRequired('A password is required')])

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[InputRequired('A username is required.'), Length(max=30, message='Username can\'t exceed 30 characters.')])
	password = PasswordField('Password', validators=[InputRequired('A password is required')])
	remember = BooleanField('Remember me') 

class ExerciseForm(FlaskForm):
	exercise_name = StringField('Exercise', validators=[InputRequired('An exercise name is required.'), Length(max=50, message='Exercise name can\'t exceed 50 characters.')])
	class Meta:
		csrf = False	# CSRF disabled for nested forms.

# Allows dynamic addition of multiple exercises to a single workout.
class AddWorkoutForm(FlaskForm):
	name = StringField('Workout name', validators=[InputRequired('A workout name is required.'), Length(max=50, message='Workout name can\'t exceed 50 characters.')])
	exercises = FieldList(FormField(ExerciseForm), min_entries=1)

class ExerciseDetails(FlaskForm):
	exercise_id = IntegerField('Exercise ID')
	sets = IntegerField('Sets', validators=[InputRequired('Sets performed is required')])
	weight = IntegerField('Weight', validators=[InputRequired('Weight is required')])
	reps = IntegerField('Reps', validators=[InputRequired('Reps performed is required')])
	class Meta:
		csrf = False	

# List of exercises performed in workout session along with stats for each exercise 
class WorkoutDetails(FlaskForm):
	exercises = FieldList(FormField(ExerciseDetails), min_entries=1) 