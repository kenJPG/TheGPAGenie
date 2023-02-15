import json
import pytest
from datetime import datetime
from urllib.parse import urlencode

# Validity REST API Testing
@pytest.mark.parametrize("inputList", [
	[1, 0, 1, 'yes', 1, 'teacher', 3, 2, 'reputation', 30, 'no', 'yes', 'no', 3],
	[2, 2, 0, 'no', 1, 'health', 3, 2, 'course', 30, 'yes', 'no', 'yes', 3],
	[3, 1, 0, 'yes', 1, 'services', 3, 2, 'home', 30, 'yes', 'yes', 'yes', 3],
	[4, 3, 1, 'no', 1, 'at_home', 3, 2, 'other', 30, 'yes', 'no', 'no', 3],
	[5, 4, 0, 'yes', 1, 'other', 3, 2, 'course', 30, 'yes', 'yes', 'yes', 3],
	[6, 2, 1, 'no', 1, 'health', 3, 2, 'reputation', 30, 'no', 'yes', 'yes', 3],
	[7, 2, 1, 'no', 1, 'health', 3, 2, 'reputation', 30, 'no', 'yes', 'yes', 3],
	[8, 1, 1, 'yes', 1, 'services', 3, 2, 'home', 30, 'no', 'no', 'no', 3],
	[9, 4, 0, 'yes', 1, 'other', 3, 2, 'course', 30, 'yes', 'yes', 'yes', 3],
	[10, 2, 1, 'no', 1, 'health', 3, 2, 'reputation', 30, 'no', 'yes', 'yes', 3],
])
def test_predAPI(client, inputList, capsys):
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

# Validity REST API Testing
@pytest.mark.parametrize("inputList", [
	*[[i] for i in range(1, 11)]
])
def test_getHistoryAPI(client, inputList, capsys):
	with capsys.disabled():

		client.set_cookie('/', 'uid', '1')
		response = client.get(
			f"/api/result/{inputList[0]}", content_type="application/json"
		)

		assert response.status_code == 200
		assert response.headers["Content-Type"] == "application/json"
		response_body = json.loads(response.get_data(as_text=True))
		assert len(response_body) == 17


# Validity REST API Testing
@pytest.mark.parametrize("filters", [
	[
		{
			'page': 0,
			'last_days': 1,
			'columns': ['failures', 'is_math', 'higher', 'health', 'Mjob', 'studytime', 'goout', 'reason', 'traveltime', 'activities', 'famsup', 'nursery', 'Total_alc'],
			'search': 'lol',
			'sort': 'predicted_on'
		}
	],
	[
		{
			'page': 2,
			'last_days': 1,
			'columns': ['failures', 'is_math', 'higher', 'health', 'Mjob', 'studytime', 'goout', 'reason', 'traveltime', 'activities', 'famsup', 'nursery', 'Total_alc'],
			'search': 'haha',
			'sort': 'predicted_on'
		}
	],
	[
		{
			'page': 0,
			'last_days': 3,
			'columns': ['failures', 'is_math', 'higher', 'health', 'Mjob', 'studytime', 'goout', 'reason', 'traveltime', 'activities', 'famsup', 'nursery', 'Total_alc'],
			'search': '5',
			'sort': 'predicted_on'
		}
	],
])
def test_getFilteredHistoryAPI(client, filters, capsys):
	with capsys.disabled():
		client.set_cookie('/', 'uid', '1')
		myarr = []
		for k, v in filters[0].items():
			if type(v) == list:
				for item in v:
					myarr.append((k, item))
			else:
				myarr.append((k, v))

		response = client.get(
			f"/api/history?" + urlencode(myarr), content_type="application/json"
		)

		assert response.status_code == 200
		assert response.headers["Content-Type"] == "application/json"
		response_body = json.loads(response.get_data(as_text=True))
		assert response_body.get('output') != None and response_body.get('output') != 'error'


# Validity REST API Testing
@pytest.mark.parametrize("histIds", list(range(1, 11)))
def test_deleteHistoryAPI(client, histIds, capsys):
	with capsys.disabled():

		client.set_cookie('/', 'uid', '1')
		response = client.delete(
			f"/api/history/{histIds}", content_type="application/json"
		)

		assert response.status_code == 200
		assert response.headers["Content-Type"] == "application/json"
		response_body = json.loads(response.get_data(as_text=True))
		assert response_body["success"] == True