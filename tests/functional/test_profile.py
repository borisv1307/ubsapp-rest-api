"""
This file (test_profile.py) contains the functional tests which
test create profile and view profile.

"""
#pylint: disable = line-too-long, too-many-lines, no-name-in-module, import-error, multiple-imports, pointless-string-statement, wrong-import-order
import pytest
import os
import sys
from flask import jsonify, request, json
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
PARENT_ROOT=os.path.abspath(os.path.join(SITE_ROOT, os.pardir))
GRANDPAPA_ROOT=os.path.abspath(os.path.join(PARENT_ROOT, os.pardir))
sys.path.insert(0,GRANDPAPA_ROOT)
from project import create_app
from project import mongo
from bson.objectid import ObjectId
from random import randint

profilename = "Profile A"

@pytest.fixture
def test_client():
    flask_app = create_app('test')
    flask_app.config['TESTING'] = True

    with flask_app.test_client() as testing_client:
        yield testing_client

class TestSomething:

    def test_for_user_id(self,test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/createProfile' page is requested (POST)
        THEN check that request has user_id
        """
        data = {
        "email": "email",
        "profileName":profilename,
        "profileImg":"https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png",
        "first_name": "Test",
        "last_name": "User",
        "position": "Developer",
        "aboutMe": "Hello World",
        "education": [
            {
            "school": "Drexel",
            "degree": "MA",
            "major": "SE",
            "eduStartDate": "0001-01",
            "eduEndDate": "0001-01",
            "gpa": "3"
            }
        ],
        "experience": [
            {
            "title": "Developer",
            "company": "ABC",
            "location": "PH",
            "expStartDate": "0001-01",
            "expEndDate": "0001-01"
            }
        ]
        }
        response = test_client.post('/api/v1/createProfile/', data=json.dumps(data),headers={'Content-Type': 'application/json'})
        assert response.status_code == 403
        assert response.data == b'{"code":4,"error":"Missing request body"}\n'

    def test_checking_a_valid_user_id_when_null(self,test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/createProfile' page is requested (POST)
        THEN check if user_id is valid (None, Whilespaces and not following pattern)
        """

        data = {
        "email": "email",
        "profileName":profilename,
        "profileImg":"https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png",
        "first_name": "Test",
        "last_name": "User",
        "position": "Developer",
        "aboutMe": "Hello World",
        "education": [
            {
            "school": "Drexel",
            "degree": "MA",
            "major": "SE",
            "eduStartDate": "0001-01",
            "eduEndDate": "0001-01",
            "gpa": "3"
            }
        ],
        "experience": [
            {
            "title": "Developer",
            "company": "ABC",
            "location": "PH",
            "expStartDate": "0001-01",
            "expEndDate": "0001-01"
            }
        ],
        "user_id": None
        }
        response = test_client.post('/api/v1/createProfile/', data=json.dumps(data),headers={'Content-Type': 'application/json'})
        assert response.status_code == 403
        assert response.data == b'{"code":4,"error":"Input fields cannot be blank or null"}\n'


    def test_checking_a_valid_user_id_with_whitespace(self,test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/createProfile' page is requested (POST)
        THEN check if user_id is valid (None, Whilespaces and not following pattern)
        """

        data = {
        "email": "email",
        "profileName":profilename,
        "profileImg":"https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png",
        "first_name": "Test",
        "last_name": "User",
        "position": "Developer",
        "aboutMe": "Hello World",
        "education": [
            {
            "school": "Drexel",
            "degree": "MA",
            "major": "SE",
            "eduStartDate": "0001-01",
            "eduEndDate": "0001-01",
            "gpa": "3"
            }
        ],
        "experience": [
            {
            "title": "Developer",
            "company": "ABC",
            "location": "PH",
            "expStartDate": "0001-01",
            "expEndDate": "0001-01"
            }
        ],
        "user_id": ' '
        }
        response = test_client.post('/api/v1/createProfile/', data=json.dumps(data),headers={'Content-Type': 'application/json'})
        assert response.status_code == 403
        assert response.data == b'{"code":4,"error":"Input fields cannot be blank or null"}\n'


    def test_create_profile(self,test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/createProfile' page is requested (POST)
        THEN check that the response is valid
        """

        data = {
        "email":"jasonmax@gmail.com",
        "profileName":profilename,
        "profileImg":"https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png",
        "first_name": "Test",
        "last_name": "User",
        "position": "Developer",
        "aboutMe": "Hello World",
        "education": [
            {
            "school": "Drexel",
            "degree": "MA",
            "major": "SE",
            "eduStartDate": "0001-01",
            "eduEndDate": "0001-01",
            "gpa": "3"
            }
        ],
        "experience": [
            {
            "title": "Developer",
            "company": "ABC",
            "location": "PH",
            "expStartDate": "0001-01",
            "expEndDate": "0001-01"
            }
        ],
        "user_id": "1"
        }
        response = test_client.post('/api/v1/createProfile/', data=json.dumps(data),headers={'Content-Type': 'application/json'})
        assert response.status_code == 200
        assert response != 'null'

    def test_createprofile_for_user_which_does_not_exist(self,test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/createProfile' page is requested (POST)
        THEN check that the response is valid
        """

        data = {
        "email":"test@test78.com",
        "profileName":profilename,
        "profileImg":"https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png",
        "first_name": "Test",
        "last_name": "User",
        "position": "Developer",
        "aboutMe": "Hello World",
        "education": [
            {
            "school": "Drexel",
            "degree": "MA",
            "major": "SE",
            "eduStartDate": "0001-01",
            "eduEndDate": "0001-01",
            "gpa": "3"
            }
        ],
        "experience": [
            {
            "title": "Developer",
            "company": "ABC",
            "location": "PH",
            "expStartDate": "0001-01",
            "expEndDate": "0001-01"
            }
        ],
        "user_id": "99999"
        }
        response = test_client.post('/api/v1/createProfile/', data=json.dumps(data),headers={'Content-Type': 'application/json'})
        assert response.status_code == 403
        assert response.data == b'{"code":2,"error":"User account does not exist"}\n'

    def test_get_profiles(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/getProfileCount' page is requested (GET)
        THEN check that the response is valid
        """

        response = test_client.get('/api/v1/getProfiles/1/',headers={'Content-Type': 'application/json'})
        assert response.status_code == 200
        assert response.data != 'null'

    def test_get_profiles_with_invalid_userid(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/getProfileCount' page is requested (GET)
        THEN check that the response is valid
        """

        response = test_client.get('/api/v1/getProfiles/999/',headers={'Content-Type': 'application/json'})
        assert response.status_code == 200
        assert response.data == b'{"count":1,"results":{"error":"User not found"}}\n'

    def test_get_profiles_when_profile_does_not_exist(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/getProfileCount' page is requested (GET)
        THEN check that the response is valid
        """

        response = test_client.get('/api/v1/getProfiles/10/',headers={'Content-Type': 'application/json'})
        assert response.status_code == 200
        assert response.data == b'{"count":1,"results":{"error":"Profiles not found"}}\n'

    
    def test_edit_profile(self,test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/createProfile' page is requested (POST)
        THEN check that the response is valid
        """

        data = {
        "profile_id": 1,
        "email":"jimmydoe@gmail.com",
        "profileName":"profilename",
        "profileImg":"https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png",
        "first_name": "first",
        "last_name": "last",
        "position": "position",
        "aboutMe": "Hardworking",
        "education": [
            {
            "school": "Drexel",
            "degree": "MA",
            "major": "SE",
            "eduStartDate": "0001-01",
            "eduEndDate": "0001-01",
            "gpa": "3"
            }
        ],
        "experience": [
            {
            "title": "Developer",
            "company": "ABC",
            "location": "PH",
            "expStartDate": "0001-01",
            "expEndDate": "0001-01"
            }
        ],
        "user_id": "1"
        }
        response = test_client.put('/api/v1/editProfile/', data=json.dumps(data),headers={'Content-Type': 'application/json'})
        assert response.status_code == 200
        assert response != 'null'


    def test_edit_profile_for_user_which_does_not_exist(self,test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/createProfile' page is requested (POST)
        THEN check that the response is valid
        """

        data = {
        "profile_id": 1,
        "email":"test@test78.com",
        "profileName":profilename,
        "profileImg":"https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png",
        "first_name": "Test",
        "last_name": "User",
        "position": "Developer",
        "aboutMe": "Hello World",
        "education": [
            {
            "school": "Drexel",
            "degree": "MA",
            "major": "SE",
            "eduStartDate": "0001-01",
            "eduEndDate": "0001-01",
            "gpa": "3"
            }
        ],
        "experience": [
            {
            "title": "Developer",
            "company": "ABC",
            "location": "PH",
            "expStartDate": "0001-01",
            "expEndDate": "0001-01"
            }
        ],
        "user_id": "99999"
        }
        response = test_client.put('/api/v1/editProfile/', data=json.dumps(data),headers={'Content-Type': 'application/json'})
        assert response.status_code == 403
        assert response.data == b'{"code":2,"error":"User account does not exist"}\n'

    