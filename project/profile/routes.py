# pylint: disable = line-too-long, unused-variable, broad-except, trailing-whitespace, cyclic-import,bare-except, missing-module-docstring, missing-function-docstring, too-many-lines, no-name-in-module, import-error, multiple-imports, pointless-string-statement, wrong-import-order, anomalous-backslash-in-string, duplicate-code
import re
from json import loads
from functools import wraps
from bson.json_util import dumps
from flask import request
from project import mongo ,token_required, get_aws_tags
from . import profile_blueprint

################
#### routes ####
################

# ALL FUTURE DATA VALIDATION


def profile_validation(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            profile_data = request.get_json()
            get_user_id = profile_data['user_id']
        except Exception:
            return {'code': 4, 'error': 'Missing request body'}, 403

        if get_user_id is None or re.search("^\s*$", str(get_user_id)):
            return {"code": 4, "error": "Input fields cannot be blank or null"}, 403
        if not str(get_user_id).isdigit():
            return {"code": 4, "error": "Input user ID is not a digit"}, 403

        return func(*args, **kwargs)
    return decorated


@profile_blueprint.route('/api/v1/createProfile/', methods=['POST'])
@token_required
@profile_validation
def create_user_profile():
   # Get fields from request body, check for missing fields

    profile_data = request.get_json()

    get_user_id = int(profile_data['user_id'])

    # Get collections
    profile = mongo.db.profile
    aws_tags = mongo.db.aws_tags

    user = mongo.db.user
    try:
        profile_id = int(profile.find().skip(
            profile.count_documents({}) - 1)[0]['profile_id'])+1
    except Exception:
        profile_id = 1

    # check if email is already in database
    user_id_exists = user.count_documents({'user_id': get_user_id})
    if user_id_exists:
        get_tags = get_aws_tags(profile_data['profileImg'])

        create_profile = profile.insert_one({
            "profile_id": profile_id,
            "user_id": get_user_id,
            "profileName": profile_data['profileName'],
            "profileImg": profile_data['profileImg'],
            "first_name": profile_data['first_name'],
            "last_name": profile_data['last_name'],
            "position": profile_data['position'],
            "aboutMe":  profile_data['aboutMe'],
            "education": profile_data['education'],
            "experience": profile_data['experience'],
            "gender": profile_data['gender'],
            "email": profile_data['email'],
            "ethnicity": profile_data['ethnicity']
        })
        create_aws_tags = aws_tags.insert_one({
            "profile_id": profile_id,
            "user_id": get_user_id,
            'AgeRange':get_tags['AgeRange'],
            'Smile':get_tags['Smile'],
            'Eyeglasses':get_tags['Eyeglasses'],
            'Sunglasses':get_tags['Sunglasses'],
            'Gender':get_tags['Gender'],
            'Beard':get_tags['Beard'],
            'Mustache':get_tags['Mustache'],
            'EyesOpen': get_tags['EyesOpen'],
            'MouthOpen': get_tags['MouthOpen'],
            'Emotions': get_tags['Emotions']
        })

        if create_profile:
            output = {
                "profile_id": profile_id,
                "user_id": get_user_id,
                "profileName": profile_data['profileName'],
                "profileImg": profile_data['profileImg'],
                "first_name": profile_data['first_name'],
                "last_name": profile_data['last_name'],
                "position": profile_data['position'],
                "aboutMe":  profile_data['aboutMe'],
                "education": profile_data['education'],
                "experience": profile_data['experience'],
                "gender": profile_data['gender'],
                "email": profile_data['email'],
                "ethnicity": profile_data['ethnicity']
            }
        else:
            output = {'code': 2, "error": "Insert Failed"}
    else:
        output = {'code': 2, "error": "User account does not exist"}, 403

    return output


@profile_blueprint.route('/api/v1/getProfiles/<user_id>/', methods=['GET'])
@token_required
def get_user_profiles(user_id):
    # Get user_id
    int_user_id = int(user_id)
    # Get collections
    userdb = mongo.db.user
    profile = mongo.db.profile
    output = []
    try:
        user = loads(dumps(userdb.find({"user_id": int_user_id})))
        profiles = loads(dumps(profile.find({"user_id": int_user_id})))
        # Check if user and profile exists if not display error message accordingly
        if user:
            if profiles:
                get_contact = user[0]['contact_details']
                for getprofile in profiles:
                    # Check if contact_details is an array or object
                    try:
                        validate_user = user[0]['contact_details']['state']
                        value = True
                    except Exception as exception_msg:
                        print(
                            "Unhandled Error inside the check condition:- %s" % exception_msg)
                        value = False
                    if value:
                        output.append({
                            "profile_id": getprofile['profile_id'],
                            "profileName": getprofile['profileName'],
                            "user_id": getprofile['user_id'],
                            "state": user[0]['contact_details']['state'],
                            "zip": user[0]['contact_details']['zip'],
                            "city": user[0]['contact_details']['city'],
                            "email": getprofile['email'],
                            "profileImg": getprofile['profileImg'],
                            "first_name": getprofile['first_name'],
                            "last_name": getprofile['last_name'],
                            "position": getprofile['position'],
                            "aboutMe":  getprofile['aboutMe'],
                            "education": getprofile['education'],
                            "experience": getprofile['experience'],
                            "gender": getprofile['gender'],
                            "ethnicity": getprofile['ethnicity']
                        })
                    else:
                        output.append({
                            "profile_id": getprofile['profile_id'],
                            "profileName": getprofile['profileName'],
                            "user_id": getprofile['user_id'],
                            "state": get_contact[0]['state'],
                            "zip": get_contact[0]['zip'],
                            "city": get_contact[0]['city'],
                            "email": getprofile['email'],
                            "profileImg": getprofile['profileImg'],
                            "first_name": getprofile['first_name'],
                            "last_name": getprofile['last_name'],
                            "position": getprofile['position'],
                            "aboutMe":  getprofile['aboutMe'],
                            "education": getprofile['education'],
                            "experience": getprofile['experience'],
                            "gender": getprofile['gender'],
                            "ethnicity": getprofile['ethnicity']
                        })
            else:
                output = {"error": "Profiles not found"}
        else:
            output = {"error": "User not found"}
        if len(output) == 0:
            output = {"error": "User not found"}
        else:
            output = {"count": len(output), "results": output}
    except Exception as exception_msg:
        print("Unhandled Error is:- %s" % exception_msg)
        output = {'code': 2, "error": "Error fetching details from DB"}
    return output

@profile_blueprint.route('/api/v1/editProfile/', methods=['PUT'])
@token_required
@profile_validation
def edit_profile():
    profile_data = request.get_json()
    get_user_id = int(profile_data['user_id'])
    get_profile_id = int(profile_data['profile_id'])
    # Get collections
    profile = mongo.db.profile
    user = mongo.db.user

    user_id_exists = user.count_documents({'user_id': get_user_id})
    if user_id_exists:
        edit_profile_action = profile.replace_one({"user_id": get_user_id, "profile_id": get_profile_id},
        {
            "profile_id": profile_data['profile_id'],
            "user_id": profile_data['user_id'],
            "profileName": profile_data["profileName"],
            "profileImg": profile_data["profileImg"],
            "first_name": profile_data["first_name"],
            "last_name": profile_data["last_name"],
            "position": profile_data["position"],
            "aboutMe": profile_data["aboutMe"],
            "education": profile_data["education"],
            "experience": profile_data["experience"],
            "gender": profile_data["gender"],
            "email": profile_data["email"],
            "ethnicity": profile_data["ethnicity"]


        })
        if edit_profile_action:
            output = {
                "profile_id": profile_data['profile_id'],
                "user_id": profile_data['user_id'],

                "profileName": profile_data["profileName"],
                "profileImg": profile_data["profileImg"],
                "first_name": profile_data["first_name"],
                "last_name": profile_data["last_name"],
                "position": profile_data["position"],
                "aboutMe": profile_data["aboutMe"],
                "education": profile_data["education"],
                "experience": profile_data["experience"],
                "gender": profile_data["gender"],
                "email": profile_data["email"],
                "ethnicity": profile_data["ethnicity"]

            }
        else:
            output = {"code": 2, "error": "Document update failed"}
    else:
        output = {'code': 2, "error": "User account does not exist"}, 403

    return output
