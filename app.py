from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, BooleanField, IntegerField, FieldList, FormField
from wtforms.validators import InputRequired, Length 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from datetime import datetime, timedelta
import jinja2 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\Tyler\\flask_app\\lifting_log\\lifting_log.db'
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'alskdjfasdfasdfkljasgjalsdfkgj' 

env = jinja2.Environment()
app.jinja_env.globals.update(zip=zip)

login_manager = LoginManager(app)
login_manager.login_view = 'login' 

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(UserMixin, db.Model):
	user_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(30))
	email = db.Column(db.String(50))
	password = db.Column(db.String(50))
	def get_id(self):
		return (self.user_id)

class Workout(db.Model):
	workout_id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
	workout_name = db.Column(db.String(50))

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

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

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
		csrf = False

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

class WorkoutDetails(FlaskForm):
	exercises = FieldList(FormField(ExerciseDetails), min_entries=1) 

@app.route('/')
def index():
	form = LoginForm()

	return render_template('home.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return redirect(url_for('index'))

	form = LoginForm()

	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first() 

		if not user:
			return render_template('home.html', form=form, message='Login Failed!')

		if check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)

			return redirect(url_for('entries'))

		return render_template('home.html', form=form, message='Login Failed!')

	return render_template('home.html', form=form)

@app.route('/entries', methods=['GET', 'POST'])
@login_required
def entries():
	form = WorkoutDetails()

	user_id = current_user.user_id
	workouts = Workout.query.filter_by(user_id=user_id).all()

	card_log = db.session.query(Workout_log).filter_by(user_id=user_id).order_by(Workout_log.log_date.desc()).all()


	selected_workout = None
	if request.method == 'POST':
		workout_id = request.form.get('workoutSelect')
		selected_workout = Workout.query.filter_by(user_id=user_id, workout_id=workout_id).first()

		if selected_workout:
			form.exercises.entries.clear()
			for exercise in selected_workout.exercises:
				exercise_form = ExerciseDetails()
				form.exercises.append_entry(exercise_form)

	return render_template('entries.html', current_user=current_user, workouts=workouts, 
											selected_workout=selected_workout, form=form, card_log=card_log)

@app.route('/log_Workout', methods=['POST'])
def log_Workout():
	form = WorkoutDetails()

	if form.validate_on_submit():
		workout_log = Workout_log(user_id=current_user.user_id, workout_id=request.form.get('workoutSelect'),log_date=datetime.now())
		db.session.add(workout_log)
		db.session.commit()

		for exercise_details in form.exercises:
			log_details = Log_details(log_id=workout_log.log_id, exercise_id=exercise_details.exercise_id.data, 
										sets=exercise_details.sets.data, weight=exercise_details.weight.data, 
										repetitions=exercise_details.reps.data)
			db.session.add(log_details)
		db.session.commit()

		return redirect(url_for('entries'))
	return render_template('entries.html', form=form)

@app.route('/logout')
@login_required 
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/addExercise')
@login_required
def addExercise():
	form = AddWorkoutForm()

	user_id = current_user.user_id
	workouts = Workout.query.filter_by(user_id=user_id).all()

	return render_template('addExercise.html', form=form, workouts=workouts)

@app.route('/submit_Workout', methods=['POST'])
@login_required
def submit_Workout():
	form = AddWorkoutForm()

	if form.validate_on_submit():
		new_workout = Workout(user_id=current_user.user_id, workout_name=form.name.data)
		db.session.add(new_workout)
		db.session.commit()

		for exercise_form in form.exercises:
			new_exercise = Exercises(workout_id=new_workout.workout_id, exercise_name=exercise_form.exercise_name.data)
			db.session.add(new_exercise)

		db.session.commit()

		return redirect(url_for('addExercise'))

	return 'Something went wrong'

@app.route('/analyze', methods=['GET', 'POST'])
@login_required
def analyze():

	user_id = current_user.user_id
	selected_name = ''
	time_range = request.form.get('time_range', '30')
	item_id = request.form.get('item_id', None)
	chart_data = []


	def workout_volumeLoad(log):
		volume = sum(amount.sets*amount.weight*amount.repetitions for amount in log.log_details)
		return volume 

	def workout_timeFilter(time_range):
		chart_data = []
		if time_range == 'all':
			all_logs = Workout_log.query.filter_by(workout_id=item_id).all()
			start_date = all_logs[0].log_date if all_logs else datetime.now()
		else:
			time = int(time_range)
			end_time = datetime.now()
			start_time = end_time - timedelta(days=time)
			all_logs = db.session.query(Workout_log).filter(Workout_log.workout_id==item_id, Workout_log.log_date.between(start_time, end_time)).all()

		for log in all_logs:
			formatted_date = log.log_date.strftime('%Y-%m-%d') 
			volume = workout_volumeLoad(log)
			chart_data.append({'x': formatted_date, 'y': volume})

		return chart_data

	def exercise_timeFilter(time_range):
		chart_data = []
		if time_range == 'all':
			all_logs = Log_details.query.filter_by(exercise_id=item_id).all()
			start_date = all_logs[0].workout_log.log_date if all_logs else datetime.now()
		else:
			time = int(time_range)
			end_time = datetime.now()
			start_time = end_time - timedelta(days=time)
			all_logs = db.session.query(Log_details).filter(Log_details.exercise_id==item_id, Log_details.workout_log.has(Workout_log.log_date.between(start_time, end_time))).all()

		for log in all_logs:
			formatted_date = log.workout_log.log_date.strftime('%Y-%m-%d')
			volume = log.sets * log.weight * log.repetitions
			chart_data.append({'x': formatted_date, 'y': volume})

		return chart_data

	workout_exercise = db.session.query(Workout).filter_by(user_id=user_id).all()

	if request.method == 'POST' and item_id: 
		item_type, item_id = item_id.split('_')
		item_id = int(item_id)

		if item_type == 'workout':
			selected_workout = Workout.query.filter_by(workout_id=item_id).first()
			selected_name = selected_workout.workout_name

			chart_data = workout_timeFilter(time_range)

		elif item_type == 'exercise':
			selected_exercise = Exercises.query.filter_by(exercise_id=item_id).first()
			selected_name = selected_exercise.exercise_name 
				
			chart_data = exercise_timeFilter(time_range) 


	return render_template('analyze.html', workout_exercise=workout_exercise, chart_data=chart_data, 
							selected_name=selected_name, time_range=time_range, item_id=item_id)


@app.route('/register', methods=['GET', 'POST']) 
def register():
	form = RegisterForm()

	if form.validate_on_submit():
		new_user = User(username=form.username.data, email=form.email.data, password=generate_password_hash(form.password.data))
		db.session.add(new_user)
		db.session.commit() 

		login_user(new_user)
		
		return redirect(url_for('entries')) 

	return render_template('register.html', form=form)

if __name__ == '__main__':
	app.run()