from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, SubmitField, RadioField, IntegerField
from wtforms.validators import Length, InputRequired, ValidationError, NumberRange

def process(form):
	form.failures.data = min(int(form.failures.data), 3)
	x = form.studytime.data
	if x < 2:
		form.studytime.data = 1
	elif x <= 5:
		form.studytime.data = 2
	elif x <= 10:
		form.studytime.data = 3
	else:
		form.studytime.data = 4

	x = form.traveltime.data
	if x < 15:
		form.traveltime.data = 1
	elif x <= 30:
		form.traveltime.data = 2
	elif x <= 60:
		form.traveltime.data = 3
	else:
		form.traveltime.data = 4 


class QuestionForm(FlaskForm):
	failures = IntegerField("How many times have you failed a module before?", validators = [NumberRange(min = 0)])
	# Process 0, 1, 2, 3, >4 -> 4

	is_math = RadioField("Are you in a course that does more math than language?",
	choices = [(1, 'Yes'), (0, 'No')])

	higher = RadioField("Do you want to go to uni?",
	choices = [('yes', 'Yes'), ('no', 'No')])

	health = RadioField("Rate your health",
	choices = [(1, 'Unhealthy'), (2, 'Could be better'), (3, 'Alright'), (4, 'Well'), (5, 'Amazing')])

	Mjob = RadioField("What is your mother's job?",
	choices = [('teacher', 'Teacher'), ('health', 'Health care related'), ('services', 'Civil service'), ('at_home', 'At Home'), ('other', 'Other')])

	studytime = IntegerField("How many hours do you study in a week?", validators = [NumberRange(min = 0)])
	# Process <2 -> 1, 2 to 5 -> 2, 5 to 10 -> 3, >10 -> 4

	goout = RadioField("How often do you go out with friends?", 
	choices = [(1, "Never"), (2, "Barely"), (3, "Ok amount"), (4, "Quite a bit"), (5, "All the time")])

	reason = RadioField("What did you choose to go to your school?",
	choices = [('home', 'Close to home'), ('reputation', 'School reputation'), ('course', 'Course preference'), ('other', 'Other')])

	traveltime = IntegerField("How many minutes does it take to go to school?", validators = [NumberRange(min = 0)])
	# Process <15 -> 1, 15 to 30 -> 2, 30 to 60 -> 3, >60 -> 4

	activities = RadioField("Any extra-curricular activities",
	choices = [('yes', 'Yes'), ('no', 'No')])

	famsup = RadioField("Does your family help you with your studies (not tuition)?",
	choices = [('yes', 'Yes'), ('no', 'No')])

	nursery = RadioField("Did you go to a nursery school?",
	choices = [('yes', 'Yes'), ('no', 'No')])

	Total_alc = IntegerField("How much alcohol do you drink? 1 (nothing) to 5 (too much)",
	validators = [NumberRange(1,5)])

	submit = SubmitField("Predict")

	def __len__(self):
		return 14

class LoginForm(FlaskForm):
	username = StringField("username", validators = [InputRequired()])
	password = PasswordField("password", validators = [InputRequired()])
	submit = SubmitField("log in")