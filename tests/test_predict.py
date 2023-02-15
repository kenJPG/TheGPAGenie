import json
import pytest
from datetime import datetime
from urllib.parse import urlencode

# Expected Failure
# - Range Error on Prediction
@pytest.mark.xfail(reason = 'Range Error')
@pytest.mark.parametrize("inputList", [
	[1, -1, 1, 'yes', 1, 'teacher', 3, 2, 'reputation', 30, 'no', 'yes', 'no', 3],
	[1, 2, 2, 'no', 1, 'health', 3, 2, 'course', 30, 'yes', 'no', 'yes', 3],
	[1, 1, -1, 'yes', 1, 'services', 3, 2, 'home', 30, 'yes', 'yes', 'yes', 3],
	[1, 1, -5, 'no', 1, 'at_home', 3, 2, 'other', 30, 'yes', 'no', 'no', 3],
	[1, 1, 10, 'yes', 1, 'other', 3, 2, 'course', 30, 'yes', 'yes', 'yes', 3],
	[1, 2, 1, 'what', 1, 'health', 3, 2, 'reputation', 30, 'no', 'yes', 'yes', 3],
	[1, 1, 1, 'es', 1, 'services', 3, 2, 'home', 30, 'no', 'no', 'no', 3],
	[1, 2, 1, 'what', 6, 'health', 3, 2, 'reputation', 30, 'no', 'yes', 'yes', 3],
	[1, 1, 1, 'yes', -1, 'services', 3, 2, 'home', 30, 'no', 'no', 'no', 3],
	[1, 2, 1, 'yes', -5, 'health', 3, 2, 'reputation', 30, 'no', 'yes', 'yes', 3],
	[1, 1, 1, 'yes', 2, 'out', 3, 2, 'home', 30, 'no', 'no', 'no', 3],
	[1, 1, 1, 'yes', 2, 'vices', 3, 2, 'home', 30, 'no', 'no', 'no', 3],
	[1, 1, 1, 'yes', 2, 'services', -1, 2, 'home', 30, 'no', 'no', 'no', 3],
	[1, 1, 1, 'yes', 2, 'services', -100, 2, 'home', 30, 'no', 'no', 'no', 3],
	[1, 1, 1, 'yes', 2, 'services', 0, -1, 'home', 30, 'no', 'no', 'no', 3],
	[1, 1, 1, 'yes', 2, 'services', 0, 6, 'home', 30, 'no', 'no', 'no', 3],
	[1, 1, 1, 'yes', 2, 'services', 0, 3, 'ome', 30, 'no', 'no', 'no', 3],
	[1, 1, 1, 'yes', 2, 'services', 0, 3, 'no', 30, 'no', 'no', 'no', 3],
	[1, 1, 1, 'yes', 2, 'services', 0, 3, 'home', -5, 'no', 'no', 'no', 3],
	[1, 1, 1, 'yes', 2, 'services', 0, 3, 'home', 30, 'ano', 'no', 'no', 3],
	[1, 1, 1, 'yes', 2, 'services', 0, 3, 'home', 30, 'n', 'no', 'no', 3],
	[1, 1, 1, 'yes', 2, 'services', 0, 3, 'home', 30, 'no', 'n', 'no', 3],
	[1, 1, 1, 'yes', 2, 'services', 0, 3, 'home', 30, 'no', 'no', 'n', 3],
	[1, 1, 1, 'yes', 2, 'services', 0, 3, 'home', 30, 'no', 'no', 'no', -1],
	[1, 1, 1, 'yes', 2, 'services', 0, 3, 'home', 30, 'no', 'no', 'no', -3],
	[1, 1, 1, 'yes', 2, 'services', 0, 3, 'home', 30, 'no', 'no', 'no', 6],
])
def test_pred(client, inputList, capsys):
	with capsys.disabled():
		columns = ['id', 'failures', 'is_math', 'higher', 'health', 'Mjob', 'studytime', 'goout', 'reason', 'traveltime', 'activities', 'famsup', 'nursery', 'Total_alc']

		data = {
			col: v for col, v in zip(columns, inputList)
		}

		client.set_cookie('/', 'uid', '1')
		response = client.post(
			"/api/predict", data=json.dumps(data), content_type = "application/json"
		)

		assert response.status_code == 200
		assert response.headers["Content-Type"] == "application/json"
		response_body = json.loads(response.get_data(as_text=True))
		assert "error" not in response_body.keys()

# Consistency testing
saved = None
@pytest.mark.parametrize("inputList", [
	[1, 0, 1, 'yes', 1, 'teacher', 3, 2, 'reputation', 30, 'no', 'yes', 'no', 3],
	[1, 0, 1, 'yes', 1, 'teacher', 3, 2, 'reputation', 30, 'no', 'yes', 'no', 3],
	[1, 0, 1, 'yes', 1, 'teacher', 3, 2, 'reputation', 30, 'no', 'yes', 'no', 3],
	[1, 0, 1, 'yes', 1, 'teacher', 3, 2, 'reputation', 30, 'no', 'yes', 'no', 3],
])
def test_predConsistent(client, inputList, capsys):
	global saved
	with capsys.disabled():
		columns = ['id', 'failures', 'is_math', 'higher', 'health', 'Mjob', 'studytime', 'goout', 'reason', 'traveltime', 'activities', 'famsup', 'nursery', 'Total_alc']

		data = {
			col: v for col, v in zip(columns, inputList)
		}

		client.set_cookie('/', 'uid', '1')
		response = client.post(
			"/api/predict", data=json.dumps(data), content_type = "application/json"
		)

		assert response.status_code == 200
		assert response.headers["Content-Type"] == "application/json"
		response_body = json.loads(response.get_data(as_text=True))

		# Store the first prediction value and use it to check
		# for the next values.
		if not saved:
			saved = response_body['prediction']

		assert saved == response_body['prediction']
		assert "error" not in response_body.keys()