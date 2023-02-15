from flask import redirect, render_template, request, session, url_for
from functools import wraps
from application.error import CustomError

def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if not ('uid' in request.cookies.keys() and request.cookies.get('uid') == '1'):
			return redirect(url_for('login'))
		return f(*args, **kwargs)
	return decorated_function

def api_token_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if not ('uid' in request.cookies.keys() and request.cookies.get('uid') == '1'):
			raise CustomError('Must be logged in to perform this action', status_code = 403)
		return f(*args, **kwargs)
	return decorated_function