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


@pytest.fixture
def test_client():
    flask_app = create_app('test')
    flask_app.config['TESTING'] = True

    with flask_app.test_client() as testing_client:
        yield testing_client

class TestDB:


    def test_db_status(self, test_client):
        """
        Test MongoDB connection
        """
        # Get collections
        users = mongo.db.profile
        profile_id = int(users.find().skip(users.count_documents({}) - 1)[0]['profile_id'])
        assert profile_id>1

    def test_profile_collection(self, test_client):
        """
        Test Profile Collection
        """
        # Get collections
        users = mongo.db.profile
        mydoc = users.find().count()
        assert mydoc>0
