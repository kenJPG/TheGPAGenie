####
# In this file, we test the retrieval and deletion of images
# along with expected errors such as invalid format and non-existent image.
##

import json
import pytest
from datetime import datetime
from urllib.parse import urlencode
import numpy as np

# Validity REST API Testing
# - Retrieve valid images
@pytest.mark.parametrize("histIds", list(range(1, 11)))
def test_getImageAPI(client, histIds, capsys):
	with capsys.disabled():

		client.set_cookie('/', 'uid', '1')

		response = client.get(
			f"/api/image/good_{histIds}.jpg", content_type="application/json"
		)

		response = client.get(
			f"/api/image/improve_{histIds}.jpg", content_type="application/json"
		)

		assert response.status_code == 200
		assert response.headers["Content-Type"] == "image/jpeg"

# Expected Failure
# - Retrieve Non-existent image
@pytest.mark.xfail(reason='get image exist fail')
@pytest.mark.parametrize("histIds", list(range(1000, 1100)))
def test_getImageAPIFail(client, histIds, capsys):
	with capsys.disabled():

		client.set_cookie('/', 'uid', '1')
		response = client.get(
			f"/api/image/good_{histIds}.jpg", content_type="application/json"
		)

		response = client.get(
			f"/api/image/improve_{histIds}.jpg", content_type="application/json"
		)

		assert response.status_code == 200
		assert response.headers["Content-Type"] == "image/jpeg"
		response_body = json.loads(response.get_data(as_text=True))
		assert response_body["success"] == True

# Expected Failure
# - Retrieve image with bad file format
@pytest.mark.xfail(reason='get image format fail')
@pytest.mark.parametrize("filenames", [
	"sef.1jf",
	"sef.gif",
	"sef...gif",
	"sefgif",
	"se.f.f.f.fgif"
])
def test_getImageAPIFail(client, filenames, capsys):
	with capsys.disabled():
		client.set_cookie('/', 'uid', '1')
		response = client.get(
			f"/api/image/{filenames}", content_type="application/json"
		)

		response = client.get(
			f"/api/image/{filenames}", content_type="application/json"
		)

		assert response.status_code == 200
		assert response.headers["Content-Type"] == "image/jpeg"

# Validity REST API Testing
# - Delete valid images
@pytest.mark.parametrize("histIds", list(range(1, 11)))
def test_deleteImageAPI(client, histIds, capsys):
	with capsys.disabled():

		client.set_cookie('/', 'uid', '1')
		response = client.delete(
			f"/api/image/good_{histIds}.jpg", content_type="application/json"
		)

		response = client.delete(
			f"/api/image/improve_{histIds}.jpg", content_type="application/json"
		)

		assert response.status_code == 200
		assert response.headers["Content-Type"] == "application/json"
		response_body = json.loads(response.get_data(as_text=True))
		assert response_body["success"] == True

# Expected Failure
# - Delete Non-existent image
@pytest.mark.xfail(reason='delete image exist fail')
@pytest.mark.parametrize("histIds", list(range(1000, 1100)))
def test_deleteImageAPIFail(client, histIds, capsys):
	with capsys.disabled():

		client.set_cookie('/', 'uid', '1')
		response = client.delete(
			f"/api/image/good_{histIds}.jpg", content_type="application/json"
		)

		response = client.delete(
			f"/api/image/improve_{histIds}.jpg", content_type="application/json"
		)

		assert response.status_code == 200
		assert response.headers["Content-Type"] == "application/json"
		response_body = json.loads(response.get_data(as_text=True))
		assert response_body["success"] == True

# Expected Failure
# - Delete image with bad file format
@pytest.mark.xfail(reason='delete image format fail')
@pytest.mark.parametrize("filenames", [
	"sef.1jf",
	"sef.gif",
	"sef...gif",
	"sefgif",
	"se.f.f.f.fgif"
])
def test_getImageAPIFail(client, filenames, capsys):
	with capsys.disabled():
		client.set_cookie('/', 'uid', '1')
		response = client.get(
			f"/api/image/{filenames}", content_type="application/json"
		)

		response = client.get(
			f"/api/image/{filenames}", content_type="application/json"
		)

		assert response.status_code == 200
		assert response.headers["Content-Type"] == "image/jpeg"