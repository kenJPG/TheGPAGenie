from flask import render_template, request, flash, make_response, redirect, url_for, send_file, json, jsonify, session, abort
from application.error import CustomError
from urllib.parse import urlencode
import traceback

from sqlalchemy import func, text


from application import db
from application.models import Entry, Result
import datetime

from application import app
from application import ai_model, extractor

from application.forms import LoginForm, QuestionForm

from application.decorators import login_required, api_token_required
import pandas as pd
import numpy as np

import os

# +========================================+
# |                                        |
# |                Config                  |
# |                                        |
# +========================================+

URL = 'http://127.0.0.1:5000'
USERNAME = 'student'
PASSWORD = 'student'

# +========================================+
# |                                        |
# |            Helper Functions            |
# |                                        |
# +========================================+

def add_entry(new_entry):
	try:
		db.session.add(new_entry)
		db.session.commit()
		return new_entry.id
	except Exception as error:
		db.session.rollback()
		flash(error, "danger")
		return False

def remove_entry(entryid):
	try:
		entry = db.get_or_404(Entry, entryid)
		db.session.delete(entry)
		db.session.commit()
		return True
	except Exception as error:
		db.session.rollback()
		return False

def update_history_plot(uid):
	history_df = pd.DataFrame(
		list(map(lambda x: [x.predicted_on, x.prediction] , Entry.query.filter_by(userid = uid).all())),
		columns = ['Date', 'GPA']
	)
	history_df = history_df.sort_values(by='Date').iloc[-min(5, len(history_df)):]

	user_fig = extractor.history(history_df)
	user_fig.savefig(f'application/data/user_{uid}.jpg')

def set_for_keys(my_dict, key_arr, val):
    """
    Set val at path in my_dict defined by the string (or serializable object) array key_arr
    """
    current = my_dict
    for i in range(len(key_arr)):
        key = key_arr[i]
        if key not in current:
            if i==len(key_arr)-1:
                current[key] = val
            else:
                current[key] = {}
        else:
            if type(current[key]) is not dict:
                print("Given dictionary is not compatible with key structure requested")
                raise ValueError("Dictionary key already occupied")

        current = current[key]

    return my_dict

def to_formatted_json(df, sep="."):
    result = []
    for _, row in df.iterrows():
        parsed_row = {}
        for idx, val in row.items():
            keys = idx.split(sep)
            parsed_row = set_for_keys(parsed_row, keys, val)

        result.append(parsed_row)
    return result

def process(df_passed):
	df = df_passed.copy()
	series = df.iloc[0]
	series['failures'] = min(int(series['failures']), 3)

	x = series['studytime']
	if x < 2:
		series['studytime'] = 1
	elif x <= 5:
		series['studytime'] = 2
	elif x <= 10:
		series['studytime'] = 3
	else:
		series['studytime'] = 4

	x = series['traveltime']
	if x < 15:
		series['traveltime'] = 1
	elif x <= 30:
		series['traveltime'] = 2
	elif x <= 60:
		series['traveltime'] = 3
	else:
		series['traveltime'] = 4

	return series.to_frame().T

# +========================================+
# |                                        |
# |             Error Handler              |
# |                                        |
# +========================================+
	
@app.errorhandler(CustomError)
def handle_invalid_usage(error):
	response = jsonify(error.to_dict())
	response.status_code = error.status_code
	return response

# +========================================+
# |                                        |
# |         Front-end Serving APIs         |
# |                                        |
# +========================================+

@app.route("/", methods = ['GET'])
@app.route("/home", methods = ['GET'])
@login_required
def index():
	return render_template("index.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()

	# Check if post request
	if request.method == 'POST':
		if form.validate_on_submit():

			username = request.form.get('username')
			password = request.form.get('password')

			if username == USERNAME and password == PASSWORD:
				resp = make_response(redirect(url_for('index')))
				resp.set_cookie('uid', '1') # Get uid and set as cookie
				return resp

			else:
				flash('Incorrect username or password')

	# Check if already logged in 
	if 'uid' in request.cookies and str(request.cookies['uid']) == '1':
		return redirect(url_for('index'))

	return render_template("login.html", form = form)

@app.route("/logout", methods=['POST'])
def logout():
	resp = make_response(redirect(url_for('index')))
	resp.set_cookie('uid', '', expires = 0) # Get uid and set as cookie
	return resp

# Handles http://127.0.0.1:500/predict
@app.route("/predict", methods=['GET','POST'])
@login_required
def predict():
	form = QuestionForm()
	if request.method == 'POST':
		if form.validate_on_submit():
			X = pd.DataFrame([[
				form.failures.data,
				form.is_math.data,
				form.higher.data,
				form.health.data,
				form.Mjob.data,
				form.studytime.data,
				form.goout.data,
				form.reason.data,
				form.traveltime.data,
				form.activities.data,
				form.famsup.data,
				form.nursery.data,
				form.Total_alc.data
			]], columns = ['failures', 'is_math', 'higher',
						   'health', 'Mjob', 'studytime', 'goout',
						   'reason', 'traveltime', 'activities',
						   'famsup', 'nursery', 'Total_alc']
			)

			try:
				all_columns = ['failures', 'is_math', 'higher', 'health', 'Mjob', 'studytime', 'goout', 'reason', 'traveltime', 'activities', 'famsup', 'nursery', 'Total_alc']
				result = ai_model.predict((process(X)))

				kwargs = {column: getattr(form, column).data for column in all_columns}

				new_entry = Entry(
					userid = 1,
					**kwargs,
					prediction = float(result[0]),
					predicted_on = datetime.datetime.utcnow()
				)

				good_insight, good_fig, improve_insight, improve_fig = extractor.extract(process(X))

				entryid = add_entry(new_entry)
				update_history_plot(str(request.cookies.get('uid'))) # Update the history plot of user

				# Save and store plots in file system
				good_path = f'good_{entryid}.jpg'
				improve_path = f'improve_{entryid}.jpg'
				good_fig.savefig(f'application/data/{good_path}')
				improve_fig.savefig(f'application/data/{improve_path}')

				new_result = Result(
					entryid = entryid,
					improve_image_path = f'api/image/{improve_path}',
					improve_title = improve_insight[0],
					improve_text = improve_insight[1],
					good_image_path = f'api/image/{good_path}',
					good_title = good_insight[0],
					good_text = good_insight[1],
					public_can_view = True
				)

				new_entryid = add_entry(new_result) # Add new result

				return redirect(url_for(f'result', entryid=str(new_entryid)))

			except Exception as e:
				flash("Input has incorrect format. Unable to predict", 'error')

		else:
			flash('Unable to predict. Please edit your response and try again.', 'error')

	return render_template("question.html",
	title="Tell Me",
	form=form, show_status = (request.method == "POST"), index=True)

# Handles http://127.0.0.1:500/profile
@app.route("/profile", methods=['GET'])
@login_required
def profile():
	change = 0

	try:
		page = request.args.get('page') or 0

		if type(page) == str:
			if page.isnumeric():
				page = int(page)
			else:
				raise Exception('Parameter "page" is in incorrect format')

		last_days = request.args.get('last_days') or 10000

		if type(last_days) == str:
			if last_days.isnumeric():
				last_days = int(last_days)
			else:
				raise Exception('Parameter "last_days" is in incorrect format')
		last_days = min(last_days, 10000)

		columns = request.args.getlist('columns') or ['failures', 'is_math', 'higher', 'health', 'Mjob', 'studytime', 'goout', 'reason', 'traveltime', 'activities', 'famsup', 'nursery', 'Total_alc']
		if type(columns) != list:
			raise Exception('Parameter "last_days" is in incorrect format')
		else:
			for i, column in enumerate(columns):
				columns[i] = str(columns[i])
				if not column in ['failures', 'is_math', 'higher', 'health', 'Mjob', 'studytime', 'goout', 'reason', 'traveltime', 'activities', 'famsup', 'nursery', 'Total_alc']:
					raise Exception(f'Parameter "column" has invalid column {column}')

		columns = list(set(columns + ['prediction', 'predicted_on', 'id']))

		search = request.args.get('search') or ''

		if ':' in search:
			search_split = search.split(':')
			if not search_split[0] in ['prediction', 'predicted_on', 'id', 'failures', 'is_math', 'higher', 'health', 'Mjob', 'studytime', 'goout', 'reason', 'traveltime', 'activities', 'famsup', 'nursery', 'Total_alc']:
				search_term = getattr(Entry, 'failures').contains(f'%-1%')
			else:
				search_term = getattr(Entry, search_split[0]).contains(f'%{search_split[1]}%')
		else:
			for i, column in enumerate(columns):
				if i == 0:
					search_term = getattr(Entry, column).contains(f'%{search}%')
				else:
					search_term = search_term | getattr(Entry, column).contains(f'%{search}%')

		start_time = datetime.date.today() - datetime.timedelta(days=int(last_days))

		query = Entry.query.filter(
			(Entry.predicted_on >= start_time) & (
				search_term
			)
		)

		sort = request.args.get('sort') or 'predicted_on'
		if not sort in ['predicted_on', 'prediction']:
			raise Exception('Parameter "sort" must be one of ["predicted_on", "prediction"]')

		query = query.order_by(getattr(Entry, sort).desc())
		query = query.offset(max(0, page))
		query = query.limit(5)

		results = {'output': list(map(lambda x: x.as_dict(columns), query.all()))}
		update_history_plot(request.cookies.get('uid'))

		try:
			change = round(pd.DataFrame(results['output']).sort_values(by='predicted_on')[['prediction']].diff().tail(1).values[0][0], 2)
		except Exception as e:
			# traceback.print_exc()
			pass

		if np.isnan(change):
			change = 0

	except Exception as e:
		pass

	return render_template("profile.html", change = change, table_data = results, args = request.args, all_columns = ['failures', 'is_math', 'higher', 'health', 'Mjob', 'studytime', 'goout', 'reason', 'traveltime', 'activities', 'famsup', 'nursery', 'Total_alc'])

# Handles deletion of history http://127.0.0.1:500/profile
@app.route("/profile/remove", methods=['POST'])
@login_required
def profile_remove():
	form = QuestionForm()
	req = request.form
	id = req['id']

	api_delete_history(id)
	api_delete_image(f'improve_{id}.jpg')
	api_delete_image(f'good_{id}.jpg')

	return profile()

# Handles http://127.0.0.1:500/result/
@app.route("/result/<entryid>", methods=['GET'])
def result(entryid):
	result_query = Result.query.filter_by(entryid = entryid).first()
	entry_query = Entry.query.filter_by(id = entryid).first()

	# Check for valid
	if result_query != None and entry_query != None:
		return render_template("result.html",
		title="Results",
		entry_query = entry_query, result_query = result_query)
	else:
		abort(404)

# Error Not Found Handler
@app.errorhandler(404)
def not_found(e):
	return render_template("404.html")

# +========================================+
# |                                        |
# |                Web APIs                |
# |                                        |
# +========================================+


# Predict API
@app.route("/api/predict", methods = ['POST'])
@api_token_required
def api_predict():
	try:
		# Retrieve data
		data = request.get_json()

		# Check if invalid datatype
		if data == None:
			raise CustomError('Invalid data format', status_code = 401)

		# Check if JSON is missing any columns
		all_columns = ['failures', 'is_math', 'higher', 'health', 'Mjob', 'studytime', 'goout', 'reason', 'traveltime', 'activities', 'famsup', 'nursery', 'Total_alc']
		for column in all_columns:
			if data.get(column) == None:
				raise CustomError(f'Missing column {column}', status_code = 403)

		# Check if anything goes wrong with the prediction
		try:
			X = pd.json_normalize(data)

			kwargs = {column: data.get(column) for column in all_columns}

			result = ai_model.predict(process(X))

			new_entry = Entry(
				userid=1,
				**kwargs,
				prediction = float(result[0]),
				predicted_on=datetime.datetime.utcnow()
			)

		except Exception as e:
			raise CustomError('Invalid data format', status_code = 402)

		good_insight, good_fig, improve_insight, improve_fig = extractor.extract(process(X))

		entryid = add_entry(new_entry)
		update_history_plot(str(request.cookies.get('uid'))) # Update the history plot of user

		# Save and store plots in file system
		good_path = f'good_{entryid}.jpg'
		improve_path = f'improve_{entryid}.jpg'
		good_fig.savefig(f'application/data/{good_path}')
		improve_fig.savefig(f'application/data/{improve_path}')

		new_result = Result(
			entryid = entryid,
			improve_image_path = f'api/image/{improve_path}',
			improve_title = improve_insight[0],
			improve_text = improve_insight[1],
			good_image_path = f'api/image/{good_path}',
			good_title = good_insight[0],
			good_text = good_insight[1],
			public_can_view = True
		)

		add_entry(new_result) # Add new result
		return jsonify({'entryid': entryid, 'prediction': float(result[0])})

	except CustomError as e:
		raise e
	except Exception as e:
		# print("Uncaught:", e)
		raise CustomError('Unexpected error occurred', status_code = 500)

# Get Image API
@app.route("/api/image/<filename>", methods = ['GET'])
def api_get_image(filename):
	try:
		# Special case if request for the user history plot
		if filename == f'user_1.jpg':
			if request.cookies.get("uid") == '1': # Second part is check if aactual user and not random UID
				update_history_plot(request.cookies.get('uid') == 1)
				return send_file(f'data/{filename}')
			else:
				raise CustomError("No permission to view image", status_code = 403)

		if not os.path.isfile(f'application/data/{filename}'):
			raise CustomError("Image does not exist", status_code = 404)

		return send_file(f'data/{filename}')

	except CustomError as e:
		raise e
	except Exception as e:
		# traceback.print_exc()
		raise CustomError('Unexpected error occurred', status_code = 500)

# Delete Image API
@app.route("/api/image/<filename>", methods = ['DELETE'])
@api_token_required
def api_delete_image(filename):
	try:
		if filename.count('.') != 1 or not (filename.split('.')[1] in ['png', 'jpg']):
			raise CustomError("Invalid image format", status_code = 400)

		if os.path.isfile(f'application/data/{filename}'):
			os.remove(f'application/data/{filename}')
			return jsonify({'success': True})
		else:
			raise CustomError("Image not found", status_code = 404)

	except CustomError as e:
		raise e

	except Exception as e:
		# traceback.print_exc()
		raise CustomError('Unexpected error occurred', status_code = 500)

# Get Result API
@app.route("/api/result/<entryid>", methods=['GET'])
def api_get_result(entryid):
	entry_query = Entry.query.filter_by(id = entryid).first()

	# Check for valid
	if entry_query != None:
		data = entry_query.__dict__
		data.pop('_sa_instance_state')
		return jsonify(data)
	else:
		raise CustomError('Entryid does not exist', status_code = 404)

# Get History Filter API
@app.route("/api/history", methods = ['GET'])
@api_token_required
def api_get_history():
	try:
		page = request.args.get('page') or 0
		if type(page) == str:
			if page.isnumeric():
				page = int(page)
			else:
				raise CustomError('Parameter "page" is in incorrect format', status_code = 400)

		last_days = request.args.get('last_days') or 10000
		if type(last_days) == str:
			if last_days.isnumeric():
				last_days = int(last_days)
			else:
				raise CustomError('Parameter "last_days" is in incorrect format', status_code = 400)

		last_days = min(last_days, 10000)

		columns = request.args.getlist('columns') or ['failures', 'is_math', 'higher', 'health', 'Mjob', 'studytime', 'goout', 'reason', 'traveltime', 'activities', 'famsup', 'nursery', 'Total_alc']
		if type(columns) != list:
			raise CustomError('Parameter "last_days" is in incorrect format', status_code = 400)
		else:
			for i, column in enumerate(columns):
				columns[i] = str(columns[i])
				if not column in ['failures', 'is_math', 'higher', 'health', 'Mjob', 'studytime', 'goout', 'reason', 'traveltime', 'activities', 'famsup', 'nursery', 'Total_alc']:
					raise CustomError(f'Parameter "column" has invalid column {column}', status_code = 400)

		columns = list(set(columns + ['prediction', 'predicted_on', 'id']))

		search = request.args.get('search') or ''

		if ':' in search:
			search_split = search.split(':')
			if not search_split[0] in ['prediction', 'predicted_on', 'id', 'failures', 'is_math', 'higher', 'health', 'Mjob', 'studytime', 'goout', 'reason', 'traveltime', 'activities', 'famsup', 'nursery', 'Total_alc']:
				search_term = getattr(Entry, 'failures').contains(f'%-1%')
			else:
				search_term = getattr(Entry, search_split[0]).contains(f'%{search_split[1]}%')

		else:
			for i, column in enumerate(columns):
				if i == 0:
					search_term = getattr(Entry, column).contains(f'%{search}%')
				else:
					search_term = search_term | getattr(Entry, column).contains(f'%{search}%')

		start_time = datetime.date.today() - datetime.timedelta(days=int(last_days))

		query = Entry.query.filter(
			(Entry.predicted_on >= start_time) & (
				search_term
			)
		)

		sort = request.args.get('sort') or 'predicted_on'
		if not sort in ['predicted_on', 'prediction']:
			raise Exception('Parameter "sort" must be one of ["predicted_on", "prediction"]')

		query = query.order_by(getattr(Entry, sort).desc())
		query = query.offset(max(0, page))
		query = query.limit(5)

		return jsonify({'output': list(map(lambda x: x.as_dict(columns), query.all()))})
	except CustomError as e:
		raise e

	except Exception as e:
		# traceback.print_exc()
		raise CustomError('Unexpected error occurred', status_code = 500)

# Delete History API
@app.route("/api/history/<id>", methods = ['DELETE'])
@api_token_required
def api_delete_history(id):
	if type(id) == int or (type(id) == str and id.isnumeric()):
		id = int(id)
	else:
		raise CustomError('Incorrect ID format', status_code = 400)

	removed = remove_entry(id)

	if removed:
		return jsonify({'success': True})
	else:
		raise CustomError('ID not found', status_code = 404)