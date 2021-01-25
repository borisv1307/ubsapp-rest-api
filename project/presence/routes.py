# pylint: disable = line-too-long, inconsistent-return-statements, unused-variable, broad-except, trailing-whitespace, cyclic-import,bare-except, missing-module-docstring, missing-function-docstring, too-many-lines, no-name-in-module, import-error, multiple-imports, pointless-string-statement, too-many-locals, wrong-import-order, anomalous-backslash-in-string
from datetime import datetime
from flask import request
from project import mongo, token_required
from pymongo.collection import ReturnDocument
from . import presence_blueprint

################
#### routes ####
################

# ALL FUTURE DATA VALIDATION


@presence_blueprint.route('/api/v1/addPresence/', methods=['POST'])
@token_required
def add_presence_to_pool():
    date_joined = datetime.utcnow()
    profile_data = request.get_json()
    presence = mongo.db.presence
    user_presence_count = presence.count_documents(
        {"$and": [{"user_id": profile_data['user_id']}, {"profile_id": profile_data['profile_id']}]})
    if user_presence_count == 0:
        output = insert_data(profile_data)
        if output != "ERROR":
            result = {
                "profile_id": profile_data['profile_id'],
                "state": profile_data['state'],
                "zip": profile_data['zip'],
                "city": profile_data['city'],
                "email": profile_data['email'],
                "position": profile_data['position'],
                "aboutMe":  profile_data['aboutMe'],
                "education": profile_data['education'],
                "experience": profile_data['experience'],
                "user_id": profile_data['user_id'],
                "profileName": profile_data['profileName'],
                "profileImg": profile_data['profileImg'],
                "first_name": profile_data['first_name'],
                "last_name": profile_data['last_name'],
                "added_on": date_joined,
                "reviewed_by": output['reviewed_by'],
                "gender": profile_data['gender'],
                "ethnicity":profile_data['ethnicity']
            }
        else:
            result = {'code': 4, "error": "User account does not exist"}, 403
    else:
        result = {'code': 4, "error": "User presence already exists"}, 403

    return result


def insert_data(profile_information):
    date_joined = datetime.utcnow()
    presence = mongo.db.presence
    print("Print Gender", profile_information['gender'])
    create_presence = presence.insert_one({
        "profile_id": profile_information['profile_id'],
        "state": profile_information['state'],
        "zip": profile_information['zip'],
        "city": profile_information['city'],
        "email": profile_information['email'],
        "user_id": profile_information['user_id'],
        "profileName": profile_information['profileName'],
        "profileImg": profile_information['profileImg'],
        "first_name": profile_information['first_name'],
        "last_name": profile_information['last_name'],
        "position": profile_information['position'],
        "aboutMe":  profile_information['aboutMe'],
        "education": profile_information['education'],
        "experience": profile_information['experience'],
        "added_on": date_joined,
        "reviewed_by": [],
        "gender": profile_information['gender'],
        "ethnicity":profile_information['ethnicity']
    })
    if create_presence:
        return profile_information
    return "ERROR"


@presence_blueprint.route('/api/v1/getAllPresence/<reviewer_id>/', methods=['GET'])
@token_required
def get_all_presence_for_reviewer(reviewer_id):
    if request.method == 'GET':
        try:
            reviewer_id = int(reviewer_id)
        except TypeError:
            return {'error': 'reviewer id must be numeric'}, 403
        presences = mongo.db.presence
        output = []
        try:
            for presence in presences.find({"reviewed_by": {"$not": {'$elemMatch': {"reviewer_id": reviewer_id}}}}):
                output.append({
                    'user_id': int(presence['user_id']),
                    'profile_id': presence['profile_id'],
                    'profile_name': presence['profileName'],
                    'profileImg': presence['profileImg'],
                    'gender': presence['gender'],
                    'ethnicity': presence['ethnicity'],
                    'state': presence['state'],
                    'zip': presence['zip'],
                    'city': presence['city'],
                    'email': presence['email'],
                    'first_name': presence['first_name'],
                    'last_name': presence['last_name'],
                    'aboutMe': presence['aboutMe'],
                    'position': presence['position'],
                    'education': presence['education'],
                    'experience': presence['experience'],
                    'reviewed_by': presence['reviewed_by']
                })
            if len(output) > 0:
                return {'count': len(output), 'results': output}
            return {'code': 4, 'error': "No more presence to be reviewed"}
        except Exception as error:
            print("Exception ", error)
            return {'code': 4, 'error': "No presence found"}, 403


@presence_blueprint.route('/api/v1/savePresenceReview/', methods=['PATCH'])
@token_required
def update_presence_with_review():
    date_joined = datetime.utcnow()
    reviewer = request.get_json()
    presence_profile_id = int(reviewer['profile_id'])
    presence_user_id = int(reviewer['user_id'])
    feedback = reviewer['feedback']
    query = {"$and": [{"user_id": presence_user_id},
                      {"profile_id": presence_profile_id}]}

    try:
        if mongo.db.presence.count_documents(query) == 1:
            profile_details = mongo.db.presence.find_one_and_update(
                query, {"$push": {'reviewed_by': feedback}}, return_document=ReturnDocument.AFTER)
            result = {
                "profile_id": profile_details['profile_id'],
                "state": profile_details['state'],
                "zip": profile_details['zip'],
                "city": profile_details['city'],
                "email": profile_details['email'],
                "position": profile_details['position'],
                "gender": profile_details['gender'],
                "ethnicity": profile_details['ethnicity'],
                "aboutMe":  profile_details['aboutMe'],
                "education": profile_details['education'],
                "experience": profile_details['experience'],
                "user_id": profile_details['user_id'],
                "profileName": profile_details['profileName'],
                "profileImg": profile_details['profileImg'],
                "first_name": profile_details['first_name'],
                "last_name": profile_details['last_name'],
                "added_on": date_joined,
                "reviewed_by": profile_details['reviewed_by']
            }
        else:
            result = {'code': 4, 'error': "User presence not found"}, 200
    except Exception as error:
        print("Exception", error)
        result = {'code': 4, 'error': error}, 403
    return result


@presence_blueprint.route('/api/v1/getCount/<reviewer_id>/', methods=['GET'])
@token_required
def get_presence_count(reviewer_id):
    try:
        reviewer_id = int(reviewer_id)
    except TypeError:
        return {'error': 'reviewer id must be numeric'}, 403

    action = "$elemMatch"

    declined_male_query = {"$and": [{"reviewed_by": {action: {
        "reviewer_id": reviewer_id, "application_status": "Declined"}}}, {"gender": "Male"}]}
    declined_female_query = {"$and": [{"reviewed_by": {action: {
        "reviewer_id": reviewer_id, "application_status": "Declined"}}}, {"gender": "Female"}]}
    declined_other_query = {"$and": [{"reviewed_by": {action: {
        "reviewer_id": reviewer_id, "application_status": "Declined"}}}, {"gender": "Other"}]}
    declined_undisclosed_query = {"$and": [{"reviewed_by": {action: {
        "reviewer_id": reviewer_id, "application_status": "Declined"}}}, {"gender": "Prefer Not To Say"}]}
    accepted_male_query = {"$and": [{"reviewed_by": {action: {
        "reviewer_id": reviewer_id, "application_status": "Accepted"}}}, {"gender": "Male"}]}
    accepted_female_query = {"$and": [{"reviewed_by": {action: {
        "reviewer_id": reviewer_id, "application_status": "Accepted"}}}, {"gender": "Female"}]}
    accepted_other_query = {"$and": [{"reviewed_by": {action: {
        "reviewer_id": reviewer_id, "application_status": "Accepted"}}}, {"gender": "Other"}]}
    accepted_undisclosed_query = {"$and": [{"reviewed_by": {action: {
        "reviewer_id": reviewer_id, "application_status": "Accepted"}}}, {"gender": "Prefer Not To Say"}]}


    declined_male_count = mongo.db.presence.count_documents(
        declined_male_query)
    declined_female_count = mongo.db.presence.count_documents(
        declined_female_query)
    declined_other_count = mongo.db.presence.count_documents(
        declined_other_query)
    declined_undisclosed_count = mongo.db.presence.count_documents(
        declined_undisclosed_query)
    accepted_male_count = mongo.db.presence.count_documents(
        accepted_male_query)
    accepted_female_count = mongo.db.presence.count_documents(
        accepted_female_query)
    accepted_other_count = mongo.db.presence.count_documents(
        accepted_other_query)
    accepted_undisclosed_count = mongo.db.presence.count_documents(
        accepted_undisclosed_query)

    try:
        result = {
            "reviewer_id": reviewer_id,
            "declined_male_count": declined_male_count,
            "declined_female_count": declined_female_count,
            "declined_other_count": declined_other_count,
            "declined_undisclosed_count": declined_undisclosed_count,
            "accepted_male_count": accepted_male_count,
            "accepted_female_count": accepted_female_count,
            "accepted_other_count": accepted_other_count,
            "accepted_undisclosed_count" : accepted_undisclosed_count
        }
    except Exception as error:
        print("Exception", error)
        result = {'code': 4, 'error': "No reviews found"}, 403
    return result


@presence_blueprint.route('/api/v1/getAcceptanceRate/<user_id>/', methods=['GET'])
@token_required
def get_acceptance_rate_for_jobseeker(user_id):
    try:
        user_id = int(user_id)
    except TypeError:
        return {'error': 'reviewer id must be numeric'}, 403

    submitted_presences = list(
        mongo.db.presence.find({"user_id": user_id}))

    result = {}

    for presence in submitted_presences:
        profile_name = presence["profileName"]
        reviewer_response = presence["reviewed_by"]

        print(profile_name)

        accepted_count = 0
        declined_count = 0

        for response in reviewer_response:
            status = response["application_status"]
            if status == "Accepted":
                accepted_count += 1
            elif status == "Declined":
                declined_count += 1

        temp = {}
        temp["accepted"] = accepted_count
        temp["declined"] = declined_count

        result[profile_name] = temp

    return result

@presence_blueprint.route('/api/v1/getCountByEthnicity/<reviewer_id>/', methods=['GET'])
@token_required
def get_presence_count_by_ethnicity(reviewer_id):
    try:
        reviewer_id = int(reviewer_id)
    except TypeError:
        return {'error': 'reviewer id must be numeric'}, 403

    action = "$elemMatch"

    declined_american_indian_query = {"$and": [{"reviewed_by": {action: {
        "reviewer_id": reviewer_id, "application_status": "Declined"}}}, {"ethnicity": "American Indian"}]}
    declined_asian_query = {"$and": [{"reviewed_by": {action: {
        "reviewer_id": reviewer_id, "application_status": "Declined"}}}, {"ethnicity": "Asian"}]}
    declined_black_american_query = {"$and": [{"reviewed_by": {action: {
        "reviewer_id": reviewer_id, "application_status": "Declined"}}}, {"ethnicity": "Black or African American"}]}
    declined_hispanic_latino__query = {"$and": [{"reviewed_by": {action: {
        "reviewer_id": reviewer_id, "application_status": "Declined"}}}, {"ethnicity": "Hispanic or Latino"}]}
    declined_pacific_islander_query = {"$and": [{"reviewed_by": {action: {
        "reviewer_id": reviewer_id, "application_status": "Declined"}}}, {"ethnicity": "Pacific Islander"}]}
    declined_white_query = {"$and": [{"reviewed_by": {action: {
        "reviewer_id": reviewer_id, "application_status": "Declined"}}}, {"ethnicity": "White"}]}
    declined_other_query = {"$and": [{"reviewed_by": {action: {
        "reviewer_id": reviewer_id, "application_status": "Declined"}}}, {"ethnicity": "Other"}]}
    declined_undisclosed_query = {"$and": [{"reviewed_by": {action: {
        "reviewer_id": reviewer_id, "application_status": "Declined"}}}, {"ethnicity": "Prefer Not To Say"}]}

    accepted_american_indian_query = {"$and": [{"reviewed_by": {action: {
        "reviewer_id": reviewer_id, "application_status": "Accepted"}}}, {"ethnicity": "American Indian"}]}
    accepted_asian_query = {"$and": [{"reviewed_by": {action: {
        "reviewer_id": reviewer_id, "application_status": "Accepted"}}}, {"ethnicity": "Asian"}]}
    accepted_black_american_query = {"$and": [{"reviewed_by": {action: {
        "reviewer_id": reviewer_id, "application_status": "Accepted"}}}, {"ethnicity": "Black or African American"}]}
    accepted_hispanic_latino_query = {"$and": [{"reviewed_by": {action: {
        "reviewer_id": reviewer_id, "application_status": "Accepted"}}}, {"ethnicity": "Hispanic or Latino"}]}
    accepted_pacific_islander_query = {"$and": [{"reviewed_by": {action: {
        "reviewer_id": reviewer_id, "application_status": "Accepted"}}}, {"ethnicity": "Pacific Islander"}]}
    accepted_white_query = {"$and": [{"reviewed_by": {action: {
        "reviewer_id": reviewer_id, "application_status": "Accepted"}}}, {"ethnicity": "White"}]}
    accepted_other_query = {"$and": [{"reviewed_by": {action: {
        "reviewer_id": reviewer_id, "application_status": "Accepted"}}}, {"ethnicity": "Other"}]}
    accepted_undisclosed_query = {"$and": [{"reviewed_by": {action: {
        "reviewer_id": reviewer_id, "application_status": "Accepted"}}}, {"ethnicity": "Prefer Not To Say"}]}


    declined_american_indian_count = mongo.db.presence.count_documents(
        declined_american_indian_query)
    declined_asian_count = mongo.db.presence.count_documents(
        declined_asian_query)
    declined_black_american_count = mongo.db.presence.count_documents(
        declined_black_american_query)
    declined_hispanic_latino_count = mongo.db.presence.count_documents(
        declined_hispanic_latino__query)
    declined_pacific_islander_count = mongo.db.presence.count_documents(
        declined_pacific_islander_query)
    declined_white_count = mongo.db.presence.count_documents(
        declined_white_query)
    declined_other_count = mongo.db.presence.count_documents(
        declined_other_query)
    declined_undisclosed_count = mongo.db.presence.count_documents(
        declined_undisclosed_query)


    accepted_american_indian_count = mongo.db.presence.count_documents(
        accepted_american_indian_query)
    accepted_asian_count = mongo.db.presence.count_documents(
        accepted_asian_query)
    accepted_black_american_count = mongo.db.presence.count_documents(
        accepted_black_american_query)
    accepted_hispanic_latino_count = mongo.db.presence.count_documents(
        accepted_hispanic_latino_query)
    accepted_pacific_islander_count = mongo.db.presence.count_documents(
        accepted_pacific_islander_query)
    accepted_white_count = mongo.db.presence.count_documents(
        accepted_white_query)
    accepted_other_count = mongo.db.presence.count_documents(
        accepted_other_query)
    accepted_undisclosed_count = mongo.db.presence.count_documents(
        accepted_undisclosed_query)


    try:
        result = {
            "reviewer_id": reviewer_id,
            "declined_american_indian_count": declined_american_indian_count,
            "declined_asian_count": declined_asian_count,
            "declined_black_american_count": declined_black_american_count,
            "declined_hispanic_latino_count": declined_hispanic_latino_count,
            "declined_pacific_islander_count": declined_pacific_islander_count,
            "declined_white_count": declined_white_count,
            "declined_other_count": declined_other_count,
            "declined_undisclosed_count": declined_undisclosed_count,

            "accepted_american_indian_count": accepted_american_indian_count,
            "accepted_asian_count": accepted_asian_count,
            "accepted_black_american_count": accepted_black_american_count,
            "accepted_hispanic_latino_count": accepted_hispanic_latino_count,
            "accepted_pacific_islander_count" : accepted_pacific_islander_count,
            "accepted_white_count": accepted_white_count,
            "accepted_other_count": accepted_other_count,
            "accepted_undisclosed_count": accepted_undisclosed_count
        }
    except Exception as error:
        print("Exception", error)
        result = {'code': 4, 'error': "No reviews found"}, 403
    return result
