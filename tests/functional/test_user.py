"""
This file (test_profile.py) contains the functional tests which
test create profile and view profile.

Command to run tests:- pytest --setup-show tests/functional

"""
import pytest, os, sys , datetime , random
from json import loads
from bson.json_util import dumps
from faker import Faker
from flask import jsonify, request, json
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
PARENT_ROOT=os.path.abspath(os.path.join(SITE_ROOT, os.pardir))
GRANDPAPA_ROOT=os.path.abspath(os.path.join(PARENT_ROOT, os.pardir))
sys.path.insert(0,GRANDPAPA_ROOT)
from project import create_app
from project import mongo
from bson.objectid import ObjectId

SET_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MDUzMzkxNjksIm5iZiI6MTYwNTMzOTE2OSwianRpIjoiNzAyMzczOGYtNjc2OS00NzdkLWFhN2ItYjAzOTcyMWQwZWJlIiwiZXhwIjoxNjA1MzQwMDY5LCJpZGVudGl0eSI6eyJpZCI6MywiZGF0ZV9qb2luZWQiOiJUaHUsIDI5IE9jdCAyMDIwIDA0OjA0OjI2IEdNVCJ9LCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MifQ.6NR0py5qQ49bI6Lt1GIp_INnlXeCgasid9NndXJuslk"



@pytest.fixture
def test_client():
    flask_app = create_app('test')
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as testing_client:
        yield testing_client


class TestSomething:

    def test_for_create_user(self, test_client):
        fake = Faker()
        """
        GIVEN a Flask application configured for testing
        WHEN the '/api/v1/createUser/' page is requested (POST)
        THEN check that the response is valid
        """
        start_date = datetime.date(1980, 1, 1)
        end_date = datetime.date(2020, 2, 1)

        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        random_date = start_date + datetime.timedelta(days=random_number_of_days)


        data = {
        "first_name":fake.first_name(),
        "last_name":fake.last_name(),
        "email":fake.email(),
        "password": "Hello",
        "registration_type": "jobSeeker",
        "gender": "Male",
        "date_of_birth": random_date,
        'email_validation':'False',
        "contact_details": {
            "address": "test Street",
            "address2": "test Street 2",
            "city": "Philadelphia",
            "state":"PA",
            "zip":"19104",
            "contact_number":"12345678"
        }
        }
        response = test_client.post('/api/v1/createUser/', data=json.dumps(data),headers={'Content-Type': 'application/json'})
        get_user= json.loads(response.data)
        get_user_details = get_user['user']['otp_delivery_status']
        assert response.status_code == 200
        assert get_user_details == 'Successfully sent email'


    def test_for_missing_user_details(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/api/v1/createUser/' page is requested (POST)
        THEN check that the response is valid
        """

        data = {
        "first_name":"testFName",
        "last_name":"testLName",
        "registrationType": "jobSeeker",
        "gender": "Male",
        "date_of_birth": "1992-10-01",
        'email_validation':'False',
        "contact_details": {
            "address": "test Street",
            "address2": "test Street 2",
            "city": "Philadelphia",
            "state":"PA",
            "zip":"19104",
            "contactNumber":"12345678"
        }
        }
        response = test_client.post('/api/v1/createUser/', data=json.dumps(data),headers={'Content-Type': 'application/json'})
        assert response.status_code == 403
        assert response.data == b'{"code":4,"error":"Missing request body"}\n'


    def test_for_invalid_user_details(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/api/v1/createUser/' page is requested (POST)
        THEN check that the response is valid
        """

        data = {
        "first_name":"",
        "last_name":"",
        "email":"test@test.com",
        "password": "Hello",
        "registration_type": "",
        "gender": "Male",
        "date_of_birth": "1992-10-01",
        'email_validation':'False',
        "contact_details": {
            "address": "test Street",
            "address2": "test Street 2",
            "city": "Philadelphia",
            "state":"PA",
            "zip":"19104",
            "contactNumber":"12345678"
        }
        }
        response = test_client.post('/api/v1/createUser/', data=json.dumps(data),headers={'Content-Type': 'application/json'})
        assert response.status_code == 403
        assert response.data == b'{"code":4,"error":"Field/s cannot be blank"}\n'


    def test_for_existing_email(self, test_client):
        fake = Faker()
        users = mongo.db.user
        user_id = 1
        getemail = users.find_one( { "user_id": int(user_id) },{ 'email': 1, '_id': 0 })

        data = {
        "first_name":fake.first_name(),
        "last_name":fake.last_name(),
        "email":getemail['email'],
        "password": "Hello",
        "registration_type": "jobSeeker",
        "gender": "Male",
        "date_of_birth": "1992-10-01",
        'email_validation':'False',
        "contact_details": {
            "address": "test Street",
            "address2": "test Street 2",
            "city": "Philadelphia",
            "state":"PA",
            "zip":"19104",
            "contactNumber":"12345678"
        }
        }
        response = test_client.post('/api/v1/createUser/', data=json.dumps(data),headers={'Content-Type': 'application/json'})
        assert response.status_code == 403
        assert response.data == b'{"code":4,"error":"Email is already in use"}\n'



    def test_for_user_login(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/api/v1/login/' page is requested (POST)
        THEN check that the response is valid
        """

        data = {
        "email":"jasonmax@gmail.com",
        "password": "Hello3"
        }
        response = test_client.post('/api/v1/login/', data=json.dumps(data),headers={'Content-Type': 'application/json'})
        assert response.status_code == 200
        assert response.data != 'null'

    def test_for_user_login_incorrect_password(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/api/v1/login/' page is requested (POST)
        THEN check that the response is valid
        """

        data = {
        "email":"jasonmax@gmail.com",
        "password": "Hello234"
        }
        response = test_client.post('/api/v1/login/', data=json.dumps(data),headers={'Content-Type': 'application/json'})
        assert response.status_code == 403
        assert response.data == b'{"code":4,"error":"Invalid password"}\n'


    def test_for_login_with_missing_details(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/api/v1/login/' page is requested (POST)
        THEN check that the response is valid
        """

        data = {
        "email":"justin97@yahoo.com"
        }

        response = test_client.post('/api/v1/login/', data=json.dumps(data),headers={'Content-Type': 'application/json'})
        assert response.status_code == 403
        assert response.data == b'{"code":4,"error":"Missing request body"}\n'


    def test_for_login_with_invalid_details(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/api/v1/login/' page is requested (POST)
        THEN check that the response is valid
        """
        data = {
        "email":"",
        "password": ""
        }

        response = test_client.post('/api/v1/login/', data=json.dumps(data),headers={'Content-Type': 'application/json'})
        assert response.status_code == 403
        assert response.data == b'{"code":4,"error":"Field/s cannot be blank"}\n'


    def test_for_login_with_unknown_details(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/api/v1/login/' page is requested (POST)
        THEN check that the response is valid
        """
        fake = Faker()
        data = {
        "email":fake.email(),
        "password": "Hello"
        }

        response = test_client.post('/api/v1/login/', data=json.dumps(data),headers={'Content-Type': 'application/json'})
        assert response.status_code == 403
        assert response.data == b'{"code":4,"error":"User not found"}\n'

    def test_get_all_users(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/api/v1/users/' page is requested (GET)
        THEN check that the response is valid
        """
        data = {
        "email":"jasonmax@gmail.com",
        "password": "Hello3"
        }
        post_response = test_client.post('/api/v1/login/', data=json.dumps(data),headers={'Content-Type': 'application/json'})
        get_token = json.loads(post_response.data)
        response = test_client.get('/api/v1/users/',headers={'Content-Type': 'application/json','Authorization':get_token['token']})
        assert response.status_code == 200
        assert response.data != 'null'

    def test_get_all_users_with_invalid_token(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/api/v1/users/' page is requested (GET)
        THEN check that the response is valid
        """

        get_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9."
        response = test_client.get('/api/v1/users/',headers={'Content-Type': 'application/json','Authorization':get_token})
        assert response.status_code == 403
        assert response.data == b'{"message":"Token is Invalid!"}\n'

    def test_get_all_users_when_token_not_provided(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/api/v1/users/' page is requested (GET)
        THEN check that the response is valid
        """
        response = test_client.get('/api/v1/users/',headers={'Content-Type': 'application/json'})
        assert response.status_code == 403
        assert response.data == b'{"message":"Token is missing!"}\n'



    def test_get_one_user(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/api/v1/users/' page is requested (GET)
        THEN check that the response is valid
        """


        response = test_client.get('/api/v1/users/1/',headers={'Content-Type': 'application/json'})
        assert response.status_code == 200
        assert response.data != 'null'

    def test_get_one_user_non_numerical_user_id(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/api/v1/users/' page is requested (GET)
        THEN check that the response is valid
        """


        response = test_client.get('/api/v1/users/one/',headers={'Content-Type': 'application/json'})
        assert response.status_code == 403
        assert response.data == b'{"code":5,"error":"id must be numerical"}\n'

    def test_delete_one_user(self, test_client):
        fake = Faker()
        """
        GIVEN a Flask application configured for testing
        WHEN the '/api/v1/createUser/' page is requested (POST)
        THEN check that the response is valid
        """


        data = {
        "first_name":fake.first_name(),
        "last_name":fake.last_name(),
        "email":fake.email(),
        "password": "Hello",
        "registration_type": "jobSeeker",
        "gender": "Male",
        "date_of_birth": "1992-10-01",
        "contact_details": {
            "address": "test Street",
            "address2": "test Street 2",
            "city": "Philadelphia",
            "state":"PA",
            "zip":"19104",
            "contact_number":"12345678"
        }
        }
        test_client.post('/api/v1/createUser/', data=json.dumps(data),headers={'Content-Type': 'application/json'})
        users = mongo.db.user
        user_id = int(users.find().skip(users.count_documents({}) - 1)[0]['user_id'])
        convert_to_str= str(user_id)
        url = '/api/v1/users/'+convert_to_str+'/'

        response = test_client.delete(url,headers={'Content-Type': 'application/json'})
        assert response.status_code == 200
        assert response.data != 'null'

    def test_delete_user_record_which_is_not_in_db(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/api/v1/users/' page is requested (DELETE)
        THEN check that the response is valid
        """

        convert_to_str= str(10000)
        url = '/api/v1/users/'+convert_to_str+'/'

        response = test_client.delete(url,headers={'Content-Type': 'application/json'})
        assert response.status_code == 403
        assert response.data == b'{"code":5,"error":"User does not exist"}\n'

    def test_for_update_user(self, test_client):
        
        """
        GIVEN a Flask application configured for testing
        WHEN the '/api/v1/users/' page is requested (PATCH)
        THEN check that the response is valid
        """
        fake = Faker()
        start_date = datetime.date(1980, 1, 1)
        end_date = datetime.date(2020, 2, 1)

        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        random_date = start_date + datetime.timedelta(days=random_number_of_days)

        data = {
        "first_name":fake.first_name(),
        "last_name":fake.last_name(),
        "email":"update@gmail.com",
        "password": "Hello",
        "registration_type": "jobSeeker",
        "gender": "Male",
        "date_of_birth": random_date,
        "contact_details": {
            "address": "test Street",
            "address2": "test Street 2",
            "city": "Philadelphia",
            "state":"PA",
            "zip":"19104",
            "contact_number":"12345678"
        }
        }
        users = mongo.db.user
        user_id = int(users.find().skip(users.count_documents({}) - 1)[0]['user_id'])
        convert_to_str= str(user_id)
        url = '/api/v1/users/'+convert_to_str+'/'

        response = test_client.patch(url, data=json.dumps(data),headers={'Content-Type': 'application/json'})

        assert response.status_code == 200
        assert response.data != 'null'

    def test_for_logout_for_user_id_without_token(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/api/v1/logout/' page is requested (POST)
        THEN check that the response is valid
        """
        number_list = []
        user_list = []

        tokens = mongo.db.authtoken
        users = mongo.db.user

        get_user_id = tokens.find({},{"user_id":1})
        for user in get_user_id:
            number_list.append(user['user_id'])

        users_without_token = users.find( { 'user_id': { '$nin': number_list } } )
        for user_without_tok in users_without_token:
            user_list.append(user_without_tok['user_id'])
        set_user_id = random.choice(user_list)

        data = {
        "user_id":set_user_id,
        "token":SET_TOKEN
        }

        response = test_client.post('/api/v1/logout/', data=json.dumps(data),headers={'Content-Type': 'application/json'})
        assert response.status_code == 403
        assert response.data == b'{"code":4,"error":"User_id does not have existing token"}\n'


    def test_for_logout_when_user_exists(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/api/v1/logout/' page is requested (POST)
        THEN check that the response is valid
        """
        tokens = mongo.db.authtoken
        get_user_id = tokens.find({},{"user_id":1})
        number_list = []
        for user in get_user_id:
            number_list.append(user['user_id'])
        set_user_id = random.choice(number_list)
        get_token = tokens.find_one( { "user_id": set_user_id },{ 'key': 1, '_id': 0 })
        get_corresponding_token = get_token['key']

        data = {
        "user_id":set_user_id,
        "token":get_corresponding_token
        }
        response = test_client.post('/api/v1/logout/', data=json.dumps(data),headers={'Content-Type': 'application/json'})
        assert response.status_code == 200
        assert response.data == b'{"success":"Successfully logged out"}\n'

    def test_for_verify_otp(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/api/v1/verify_otp/' page is requested (POST)
        THEN check that the response is valid
        """
        number_list = []
        user_list = []

        otp = mongo.db.users_otp
        users = mongo.db.user

        get_user_id = otp.find({},{"user_id":1})
        for user in get_user_id:
            number_list.append(user['user_id'])

        users_with_otp = users.find( { 'user_id': { '$in': number_list } } )
        for user_with_tok in users_with_otp:
            user_list.append(user_with_tok['user_id'])
        set_user_id = random.choice(user_list)
        get_otp = otp.find_one( { "user_id": set_user_id },{ 'otp': 1, '_id': 0 })
        get_corresponding_otp = get_otp['otp']

        data = {
        "user_id":set_user_id,
        "otp":get_corresponding_otp
        }

        response = test_client.post('/api/v1/verify_otp/', data=json.dumps(data),headers={'Content-Type': 'application/json'})
        assert response.status_code == 200
        assert response.data == b'{"success":"Email validation successful"}\n'

    def test_for_resend_otp(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/api/v1/resend_otp/' page is requested (POST)
        THEN check that the response is valid
        """

        data = {
            "email": "jgeorge69@dxc.com"
               }

        response = test_client.post('/api/v1/resend_otp/', data=json.dumps(data),headers={'Content-Type': 'application/json'})
        assert response.status_code == 200
        assert response.data == b'{"success":"OTP sent via email"}\n'

    def test_for_resend_otp_when_email_not_found(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/api/v1/resend_otp/' page is requested (POST)
        THEN check that the response is valid
        """

        data = {
               "email": "jgeorge69@some.com"
               }

        response = test_client.post('/api/v1/resend_otp/', data=json.dumps(data),headers={'Content-Type': 'application/json'})
        assert response.status_code == 403
        assert response.data == b'{"code":2,"error":"Email not found"}\n'
    
    def test_for_verify_otp_when_user_id_does_not_have_otp(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/api/v1/verify_otp/' page is requested (POST)
        THEN check that the response is valid
        """
        number_list = []
        user_list = []

        otp = mongo.db.users_otp
        users = mongo.db.user

        get_user_id = otp.find({},{"user_id":1})
        for user in get_user_id:
            number_list.append(user['user_id'])

        users_with_otp = users.find( { 'user_id': { '$in': number_list } } )
        for user_with_tok in users_with_otp:
            user_list.append(user_with_tok['user_id'])
        set_user_id = random.choice(user_list)

        data = {
        "user_id": set_user_id,
        "otp": 'fbLGnQruBM'
        }

        response = test_client.post('/api/v1/verify_otp/', data=json.dumps(data),headers={'Content-Type': 'application/json'})
        assert response.status_code == 403
        assert response.data == b'{"code":4,"error":"User_id and OTP mismatch"}\n'

    def test_for_verify_otp_when_user_id_does_not_exist(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/api/v1/verify_otp/' page is requested (POST)
        THEN check that the response is valid
        """
        try:
            users = mongo.db.user
            user_id = int(users.find().skip(users.count_documents({}) - 1)[0]['user_id']) + 10
        except:
            user_id= 100000


        data = {
        "user_id":user_id,
        "otp":'jdhd@RT'
        }

        response = test_client.post('/api/v1/verify_otp/', data=json.dumps(data),headers={'Content-Type': 'application/json'})
        assert response.status_code == 403
        assert response.data == b'{"code":4,"error":"User_id does not exist"}\n'
    
    def test_for_verify_otp_when_user_id_not_an_integer(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/api/v1/verify_otp/' page is requested (POST)
        THEN check that the response is valid
        """
        
        data = {
        "user_id":"one",
        "otp":SET_TOKEN
        }

        response = test_client.post('/api/v1/verify_otp/', data=json.dumps(data),headers={'Content-Type': 'application/json'})
        assert response.status_code == 403
        assert response.data == b'{"error":"user_id must be numerical"}\n'
    
    def test_for_verify_otp_when_otp_is_blank(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/api/v1/verify_otp/' page is requested (POST)
        THEN check that the response is valid
        """
        
        data = {
        "user_id":"6",
        "otp":"  "
        }

        response = test_client.post('/api/v1/verify_otp/', data=json.dumps(data),headers={'Content-Type': 'application/json'})
        assert response.status_code == 403
        assert response.data == b'{"error":"OTP cannot be blank or null"}\n'

    def test_for_verify_otp_without_passing_user_id(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/api/v1/logout/' page is requested (POST)
        THEN check that the response is valid
        """
        
        data = {
        
        }

        response = test_client.post('/api/v1/verify_otp/', data=json.dumps(data),headers={'Content-Type': 'application/json'})
        print(response.data)
        assert response.status_code == 403
        assert response.data == b'{"error":"Missing request body"}\n'

    def test_for_logout_when_user_does_not_exist(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/api/v1/logout/' page is requested (POST)
        THEN check that the response is valid
        """
        try:
            users = mongo.db.user
            user_id = int(users.find().skip(users.count_documents({}) - 1)[0]['user_id']) + 10
        except:
            user_id= 100000
        
        data = {
        "user_id":user_id,
        "token":SET_TOKEN
        }
        
        response = test_client.post('/api/v1/logout/', data=json.dumps(data),headers={'Content-Type': 'application/json'})
        assert response.status_code == 403
        assert response.data == b'{"code":4,"error":"User_id does not exist"}\n'

    def test_for_logout_without_passing_user_id(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/api/v1/logout/' page is requested (POST)
        THEN check that the response is valid
        """
        
        data = {
        
        }

        response = test_client.post('/api/v1/logout/', data=json.dumps(data),headers={'Content-Type': 'application/json'})
        assert response.status_code == 403
        assert response.data == b'{"error":"Missing request body"}\n'
        
    def test_for_logout_when_user_id_not_an_integer(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/api/v1/logout/' page is requested (POST)
        THEN check that the response is valid
        """
        
        data = {
        "user_id":"one",
        "token":SET_TOKEN
        }

        response = test_client.post('/api/v1/logout/', data=json.dumps(data),headers={'Content-Type': 'application/json'})
        assert response.status_code == 403
        assert response.data == b'{"error":"user_id must be numerical"}\n'

    def test_for_logout_when_token_is_blank(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/api/v1/logout/' page is requested (POST)
        THEN check that the response is valid
        """
        
        data = {
        "user_id":"6",
        "token":"  "
        }

        response = test_client.post('/api/v1/logout/', data=json.dumps(data),headers={'Content-Type': 'application/json'})
        assert response.status_code == 403
        assert response.data == b'{"error":"Token cannot be blank or null"}\n'

    def test_for_logout_when_token_is_null(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/api/v1/logout/' page is requested (POST)
        THEN check that the response is valid
        """
        setnull = None
        data = {
        "user_id":"6",
        "token": setnull
        }

        response = test_client.post('/api/v1/logout/', data=json.dumps(data),headers={'Content-Type': 'application/json'})
        assert response.status_code == 403
        assert response.data == b'{"error":"Token cannot be blank or null"}\n'
