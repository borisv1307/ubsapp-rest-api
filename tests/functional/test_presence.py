"""
This file (test_profile.py) contains the functional tests which
test create profile and view profile.

"""
# pylint: disable = line-too-long, too-many-lines, no-name-in-module, import-error, multiple-imports, pointless-string-statement, wrong-import-order

import pytest
import os
import sys
from flask import jsonify, request, json
from datetime import datetime
import random
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
PARENT_ROOT = os.path.abspath(os.path.join(SITE_ROOT, os.pardir))
GRANDPAPA_ROOT = os.path.abspath(os.path.join(PARENT_ROOT, os.pardir))
sys.path.insert(0, GRANDPAPA_ROOT)
from project import create_app
from bson.objectid import ObjectId

profilename = "Profile B"

login_data = {
        "email":"mariahill@proctor-hopkins.com",
        "password": "Hello"
}
login_data_2 = {
        "email":"jflynn@gmail.com",
        "password": "Hello"
}
login_data_3 = {
        "email":"renee78@simmons.com",
        "password": "Hello"
}
login_data_4 = {
        "email":"vanessa40@hotmail.com",
        "password": "Hello"
}


@pytest.fixture
def test_client():
    flask_app = create_app('test')
    flask_app.config['TESTING'] = True

    with flask_app.test_client() as testing_client:
        yield testing_client


class TestPool:

    def test_for_adding_presence_for_pool(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/addPresence' page is requested (POST)
        THEN check that request has email address
        """
        random_userid = random.randint(99, 999999)
        random_profileid = random.randint(99, 99999)
        data = {
            "profileName": profilename,
            "gender": "Female",
            "user_id": random_userid,
            "profile_id": random_profileid,
            "state": "PA",
            "zip": "19000",
            "city": "Philadelphia",
            "email": "test@test.com",
            "profileImg": "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png",
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
            "reviewed_by": [
                {
                    "reviewed_by": "",
                    "reviewed_on": "",
                    "status": ""
                }
            ],
            "added_on": datetime.utcnow(),
            "gender": "Male",
            "ethnicity": "White"
        }
        post_response = test_client.post('/api/v1/login/', data=json.dumps(login_data),headers={'Content-Type': 'application/json'})
        get_token = json.loads(post_response.data)
        response = test_client.post(
            '/api/v1/addPresence/', data=json.dumps(data), headers={'Content-Type': 'application/json','Authorization':get_token['token']})
        assert response.status_code == 200
        assert response != 'null'

    def test_for_validating_presence_existance(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/addPresence' page is requested (POST)
        THEN check that request has email address
        """
        data = {
            "gender": "Female",
            "profileName": profilename,
            "user_id": 1,
            "profile_id": 9,
            "state": "PA",
            "zip": "19000",
            "city": "Philadelphia",
            "email": "test@test.com",
            "profileImg": "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png",
            "first_name": "Test",
            "last_name": "User",
            "position": "Developer",
            "aboutMe": "gender",
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
            "reviewed_by": [],
            "added_on": datetime.utcnow(),
            "gender": "Male",
            "ethnicity": "White"
        }
        post_response = test_client.post('/api/v1/login/', data=json.dumps(login_data_2),headers={'Content-Type': 'application/json'})
        get_token = json.loads(post_response.data)
        response = test_client.post(
            '/api/v1/addPresence/', data=json.dumps(data), headers={'Content-Type': 'application/json','Authorization':get_token['token']})
        assert response.status_code == 403
        assert response.data == b'{"code":4,"error":"User presence already exists"}\n'

    def test_get_all_presence_to_be_reviewed(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/api/v1/getAllPresence/' page is requested (POST)
        THEN check that the response is valid
        """
        post_response = test_client.post('/api/v1/login/', data=json.dumps(login_data_3),headers={'Content-Type': 'application/json'})
        get_token = json.loads(post_response.data)
        response = test_client.get(
            '/api/v1/getAllPresence/7/', headers={'Content-Type': 'application/json','Authorization':get_token['token']})
        assert response.status_code == 200
        assert response.data != b'{"code":4,"error":"No presence found"}\n'


    def test_save_presence_feedback(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/api/v1/getAllPresence/' page is requested (POST)
        THEN check that the response is valid
        """
        data = {
            "profile_id": "9",
            "user_id": "1",
            "feedback": {
                "reviewer_id": 4,
                "reviewed_on": "1122",
                "application_status": "Accepted"
            }
        }
        post_response = test_client.post('/api/v1/login/', data=json.dumps(login_data_4),headers={'Content-Type': 'application/json'})
        get_token = json.loads(post_response.data)
        response = test_client.patch('/api/v1/savePresenceReview/', data=json.dumps(
            data), headers={'Content-Type': 'application/json','Authorization':get_token['token']})
        assert response.status_code == 200
        assert response.data != b'{"code":4,"error":"No presence found"}\n'

    def test_validating_save_presence_feedback(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/api/v1/getAllPresence/' page is requested (POST)
        THEN check that the response is valid
        """
        data = {
            "profile_id": "93",
            "user_id": "71",
            "feedback": {
                "reviewer_id": 4,
                "reviewed_on": "1122",
                "application_status": "Declined"
            }
        }
        post_response = test_client.post('/api/v1/login/', data=json.dumps(login_data),headers={'Content-Type': 'application/json'})
        get_token = json.loads(post_response.data)
        response = test_client.patch('/api/v1/savePresenceReview/', data=json.dumps(
            data), headers={'Content-Type': 'application/json', 'Authorization':get_token['token']})
        assert response.status_code == 200
        assert response.data == b'{"code":2,"error":"User presence not found"}\n'

    # def test_for_get_all_presence_when_user_id_not_an_integer(self, test_client):
    #     """
    #     GIVEN a Flask application configured for testing
    #     WHEN the '/api/v1/getAllPresence/' page is requested (POST)
    #     THEN check that the response is valid
    #     """
    #
    #     response = test_client.get(
    #         '/api/v1/getAllPresence/Seven/', headers={'Content-Type': 'application/json'})
    #     assert response.status_code == 403
    #     assert response.data == b'{"error":"reviewer id must be numeric"}\n'

    def test_for_get_count(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/api/v1/getCount/' page is requested (POST)
        THEN check that the response is valid
        """
        post_response = test_client.post('/api/v1/login/', data=json.dumps(login_data_2),headers={'Content-Type': 'application/json'})
        get_token = json.loads(post_response.data)
        response = test_client.get(
            '/api/v1/getCount/4/', headers={'Content-Type': 'application/json','Authorization':get_token['token']})
        assert response.status_code == 200
        assert response.data != b'{"error": "No presence found"}\n'

    def test_for_get_count_for_each_batch(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/api/v1/getCount/' page is requested (POST)
        THEN check that the response is valid
        """
        post_response = test_client.post('/api/v1/login/', data=json.dumps(login_data_3),headers={'Content-Type': 'application/json'})
        get_token = json.loads(post_response.data)
        response = test_client.get(
            '/api/v1/getCount/4/1/', headers={'Content-Type': 'application/json','Authorization':get_token['token']})
        assert response.status_code == 200
        assert response.data != b'{"error": "No presence found"}\n'

    def test_for_get_count_batch_validation(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/api/v1/getCount/' page is requested (POST)
        THEN check that the response is valid
        """
        post_response = test_client.post('/api/v1/login/', data=json.dumps(login_data_4),headers={'Content-Type': 'application/json'})
        get_token = json.loads(post_response.data)
        response = test_client.get(
            '/api/v1/getCount/99/1/', headers={'Content-Type': 'application/json','Authorization':get_token['token']})
        assert response.status_code == 200

    def test_for_get_acceptance_rate(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/api/v1/getAcceptanceRate/' page is requested (POST)
        THEN check that the response is valid
        """
        post_response = test_client.post('/api/v1/login/', data=json.dumps(login_data),headers={'Content-Type': 'application/json'})
        get_token = json.loads(post_response.data)
        response = test_client.get(
            '/api/v1/getAcceptanceRate/1/', headers={'Content-Type': 'application/json', 'Authorization':get_token['token']})
        assert response.status_code == 200


    def test_for_get_count_by_ethnicity_batch_validation(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/api/v1/getCount/' page is requested (POST)
        THEN check that the response is valid
        """
        post_response = test_client.post('/api/v1/login/', data=json.dumps(login_data_2),headers={'Content-Type': 'application/json'})
        get_token = json.loads(post_response.data)
        response = test_client.get(
            '/api/v1/getCount/Ethnicity/99/1/', headers={'Content-Type': 'application/json','Authorization':get_token['token']})
        assert response.status_code == 200

    def test_for_get_count_by_ethnicity(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/api/v1/getAllPresence/' page is requested (POST)
        THEN check that the response is valid
        """
        post_response = test_client.post('/api/v1/login/', data=json.dumps(login_data_3),headers={'Content-Type': 'application/json'})
        get_token = json.loads(post_response.data)
        response = test_client.get(
            '/api/v1/getCountByEthnicity/99/', headers={'Content-Type': 'application/json','Authorization':get_token['token']})
        assert response.status_code == 200

    def test_for_getAllBatches(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/api/v1/getAllBatches/' page is requested (GET)
        THEN check that the response is valid
        """
        post_response = test_client.post('/api/v1/login/', data=json.dumps(login_data_4),headers={'Content-Type': 'application/json'})
        get_token = json.loads(post_response.data)
        response = test_client.get(
            '/api/v1/getAllBatches/4/', headers={'Content-Type': 'application/json','Authorization':get_token['token']})
        assert response.status_code == 200
