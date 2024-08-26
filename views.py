from app import app, db
from models import User, Workout, Exercises, Workout_log, Log_details
from forms import RegisterForm, LoginForm, ExerciseForm, AddWorkoutForm, ExerciseDetails, WorkoutDetails
from flask import render_template, redirect, url_for, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from flask_login import login_user, login_required, current_user, logout_user

# Displays login form
@app.route('/')
def index():
	form = LoginForm()
	return render_template('home.html', form=form)

# Handles user authentication
@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return redirect(url_for('index'))		# Redirect to home if accessed via GET

	form = LoginForm()

	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first() 

		if not user:
			return render_template('home.html', form=form, message='Login Failed!')

		if check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data) 		# Logs in the user 
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
		db.session.commit()				# Saves new workout and exercises to the database

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

	# Function to filter the workouts by a time range
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
			all_logs = db.session.query(Log_details).filter(Log_details.exercise_id==item_id,
						 Log_details.workout_log.has(Workout_log.log_date.between(start_time, end_time))).all()

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
		login_user(new_user)		# Log in the user after successful registration 
		return redirect(url_for('entries')) 
	return render_template('register.html', form=form)