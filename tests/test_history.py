from application.models import Entry
from datetime import datetime
import pytest
from flask import json

# Validity Testing
@pytest.mark.parametrize("entrylist", [
	[1, 0, 1, 'yes', 1, 'teacher', 3, 2, 'reputation', 30, 'no', 'yes', 'no', 3, 3.5, datetime.now()],
	[1, 2, 0, 'no', 1, 'health', 3, 2, 'course', 30, 'yes', 'no', 'yes', 3, 2.5, datetime.now()],
	[1, 1, 0, 'yes', 1, 'services', 3, 2, 'home', 30, 'yes', 'yes', 'yes', 3, 2.5, datetime.now()],
	[1, 3, 1, 'no', 1, 'at_home', 3, 2, 'other', 30, 'yes', 'no', 'no', 3, 0, datetime.now()],
	[1, 4, 0, 'yes', 1, 'other', 3, 2, 'course', 30, 'yes', 'yes', 'yes', 3, 4, datetime.now()],
	[1, 2, 1, 'no', 1, 'health', 3, 2, 'reputation', 30, 'no', 'yes', 'yes', 3, 1.0, datetime.now()],
	[1, 1, 1, 'yes', 1, 'services', 3, 2, 'home', 30, 'no', 'no', 'no', 3, 3.0, datetime.now()],
])
def test_EntryClass(entrylist, capsys):
	with capsys.disabled():
		new_entry = Entry(
			userid = entrylist[0],
			failures = entrylist[1],
			is_math = entrylist[2],
			higher = entrylist[3],
			health = entrylist[4],
			Mjob = entrylist[5],
			studytime = entrylist[6],
			goout = entrylist[7],
			reason = entrylist[8],
			traveltime = entrylist[9],
			activities = entrylist[10],
			famsup = entrylist[11],
			nursery = entrylist[12],
			Total_alc = entrylist[13],
			prediction = entrylist[14],
			predicted_on = entrylist[15]
		)

		assert new_entry.userid == entrylist[0]
		assert new_entry.failures == entrylist[1]
		assert new_entry.is_math == entrylist[2]
		assert new_entry.higher == entrylist[3]
		assert new_entry.health == entrylist[4]
		assert new_entry.Mjob == entrylist[5]
		assert new_entry.studytime == entrylist[6]
		assert new_entry.goout == entrylist[7]
		assert new_entry.reason== entrylist[8]
		assert new_entry.traveltime == entrylist[9]
		assert new_entry.activities == entrylist[10]
		assert new_entry.famsup == entrylist[11]
		assert new_entry.nursery == entrylist[12]
		assert new_entry.Total_alc == entrylist[13]
		assert new_entry.prediction == entrylist[14]
		assert new_entry.predicted_on == entrylist[15]

# Expected Failure
# - Out of range
@pytest.mark.xfail(reason='entry range fail')
@pytest.mark.parametrize('entrylist', [
	[1, -1, 1, 'yes', 1, 'teacher', 3, 2, 'reputation', 30, 'no', 'yes', 'no', 3, 3.5, datetime.now()],
	[1, 2, 2, 'no', 1, 'health', 3, 2, 'course', 30, 'yes', 'no', 'yes', 3, 2.5, datetime.now()],
	[1, 1, -1, 'yes', 1, 'services', 3, 2, 'home', 30, 'yes', 'yes', 'yes', 3, 2.5, datetime.now()],
	[1, 1, -5, 'no', 1, 'at_home', 3, 2, 'other', 30, 'yes', 'no', 'no', 3, 0, datetime.now()],
	[1, 1, 10, 'yes', 1, 'other', 3, 2, 'course', 30, 'yes', 'yes', 'yes', 3, 4, datetime.now()],
	[1, 2, 1, 'what', 1, 'health', 3, 2, 'reputation', 30, 'no', 'yes', 'yes', 3, 1.0, datetime.now()],
	[1, 1, 1, 'es', 1, 'services', 3, 2, 'home', 30, 'no', 'no', 'no', 3, 3.0, datetime.now()],
	[1, 2, 1, 'what', 6, 'health', 3, 2, 'reputation', 30, 'no', 'yes', 'yes', 3, 1.0, datetime.now()],
	[1, 1, 1, 'yes', -1, 'services', 3, 2, 'home', 30, 'no', 'no', 'no', 3, 3.0, datetime.now()],
	[1, 2, 1, 'yes', -5, 'health', 3, 2, 'reputation', 30, 'no', 'yes', 'yes', 3, 1.0, datetime.now()],
	[1, 1, 1, 'yes', 2, 'out', 3, 2, 'home', 30, 'no', 'no', 'no', 3, 3.0, datetime.now()],
	[1, 1, 1, 'yes', 2, 'vices', 3, 2, 'home', 30, 'no', 'no', 'no', 3, 3.0, datetime.now()],
	[1, 1, 1, 'yes', 2, 'services', -1, 2, 'home', 30, 'no', 'no', 'no', 3, 3.0, datetime.now()],
	[1, 1, 1, 'yes', 2, 'services', -100, 2, 'home', 30, 'no', 'no', 'no', 3, 3.0, datetime.now()],
	[1, 1, 1, 'yes', 2, 'services', 0, -1, 'home', 30, 'no', 'no', 'no', 3, 3.0, datetime.now()],
	[1, 1, 1, 'yes', 2, 'services', 0, 6, 'home', 30, 'no', 'no', 'no', 3, 3.0, datetime.now()],
	[1, 1, 1, 'yes', 2, 'services', 0, 3, 'ome', 30, 'no', 'no', 'no', 3, 3.0, datetime.now()],
	[1, 1, 1, 'yes', 2, 'services', 0, 3, 'no', 30, 'no', 'no', 'no', 3, 3.0, datetime.now()],
	[1, 1, 1, 'yes', 2, 'services', 0, 3, 'home', -5, 'no', 'no', 'no', 3, 3.0, datetime.now()],
	[1, 1, 1, 'yes', 2, 'services', 0, 3, 'home', 30, 'ano', 'no', 'no', 3, 3.0, datetime.now()],
	[1, 1, 1, 'yes', 2, 'services', 0, 3, 'home', 30, 'n', 'no', 'no', 3, 3.0, datetime.now()],
	[1, 1, 1, 'yes', 2, 'services', 0, 3, 'home', 30, 'no', 'n', 'no', 3, 3.0, datetime.now()],
	[1, 1, 1, 'yes', 2, 'services', 0, 3, 'home', 30, 'no', 'no', 'n', 3, 3.0, datetime.now()],
	[1, 1, 1, 'yes', 2, 'services', 0, 3, 'home', 30, 'no', 'no', 'no', -1, 3.0, datetime.now()],
	[1, 1, 1, 'yes', 2, 'services', 0, 3, 'home', 30, 'no', 'no', 'no', -3, 3.0, datetime.now()],
	[1, 1, 1, 'yes', 2, 'services', 0, 3, 'home', 30, 'no', 'no', 'no', 6, 3.0, datetime.now()],
	[1, 1, 1, 'yes', 2, 'services', 0, 3, 'home', 30, 'no', 'no', 'no', 3, -3.0, datetime.now()],
	[1, 1, 1, 'yes', 2, 'services', 0, 3, 'home', 30, 'no', 'no', 'no', 3, 5.0, datetime.now()],
	[1, 1, 1, 'yes', 2, 'services', 0, 3, 'home', 30, 'no', 'no', 'no', 3, 4.1, datetime.now()],
])
def test_EntryRange(entrylist, capsys):
	test_EntryClass(entrylist, capsys)

def gen_dt_list(entrylist): # Generator functions to generate bad values
	gen_list = []
	for i in range(0, len(entrylist[0])):
		x = entrylist[0][i]
		new_list = [*entrylist[0]]
		new_list[i] = 'number' if type(x) == int or type(x) == float else 4
		gen_list.append(new_list)
	return gen_list

# Expected Failure
# - Wrong data type
@pytest.mark.xfail(reason='entry data type fail')
@pytest.mark.parametrize('entrylist', gen_dt_list([
	[1, 1, 1, 'yes', 2, 'services', 0, 3, 'home', 30, 'no', 'no', 'no', 3, 3, datetime.now()],
]))
def test_EntryDataType(entrylist, capsys):
	test_EntryClass(entrylist, capsys)

# Expected Failure
# - Null value
def gen_null_list(entrylist): # Generator functions to generate bad values
	gen_list = []
	for i in range(0, len(entrylist[0])):
		new_list = [*entrylist[0]]
		new_list[i] = None
		gen_list.append(new_list)
	return gen_list

def gen_empty_string_list(entrylist): # Generator functions to generate bad values
	gen_list = []
	for i in range(0, len(entrylist[0])):
		new_list = [*entrylist[0]]
		new_list[i] = ''
		gen_list.append(new_list)
	return gen_list

@pytest.mark.xfail(reason = 'entry null data')
@pytest.mark.parametrize('entrylist', gen_null_list([
	[1, 1, 1, 'yes', 2, 'services', 0, 3, 'home', 30, 'no', 'no', 'no', 3, 3, datetime.now()],
]) + gen_empty_string_list([
	[1, 1, 1, 'yes', 2, 'services', 0, 3, 'home', 30, 'no', 'no', 'no', 3, 3, datetime.now()]
]))
def test_EntryNull(entrylist, capsys):
	test_EntryClass(entrylist, capsys)