#pylint: disable = missing-function-docstring ,import-outside-toplevel, trailing-whitespace ,missing-module-docstring, missing-final-newline, missing-module-docstring, missing-function-docstring, line-too-long, too-many-lines, no-name-in-module, import-error, multiple-imports, pointless-string-statement, wrong-import-order
from flask import Flask,jsonify,request
from flask_pymongo import PyMongo
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from functools import wraps
import boto3, requests


SET_KEY = 'abcdefghijklmnopqrstuvwxyz'
BATCH_COUNT = 10

mongo = PyMongo()

def create_app(env_name):

    # Flask Config
    app = Flask(__name__)
    initialize_extensions(app,env_name)
    register_blueprints(app)
    return app

def initialize_extensions(app,env_name):
    CORS(app)
    JWTManager(app)
    app.config['JWT_SECRET_KEY'] = 'secret'
    if env_name =='dev':
        app.config['MONGO_URI'] = "mongodb+srv://UBSDBAdmin:Admin123@cluster0.yed1w.azure.mongodb.net/UBSDB?ssl=true&ssl_cert_reqs=CERT_NONE"
    else:
        app.config['MONGO_URI'] = "mongodb+srv://UBSDBAdmin:Admin123@cluster0.yed1w.azure.mongodb.net/UBSDBTEST?ssl=true&ssl_cert_reqs=CERT_NONE"
    mongo.init_app(app)

### TOKEN REQUIRED DECORATOR
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            header_token = request.headers['Authorization']
        except Exception:
            return jsonify({'message': 'Token is missing!'}), 403

        tokens = mongo.db.authtoken
        if not tokens.find_one({'key': header_token}):
            return jsonify({'message': 'Token is Invalid!'}), 403
        return f(*args, **kwargs)
    return decorated

def encrypt(n, plaintext):
    """Encrypt the string and return the ciphertext"""
    result = ''

    for l in plaintext.lower():
        try:
            i = (SET_KEY.index(l) + n) % 26
            result += SET_KEY[i]
        except ValueError:
            result += l

    return result.lower()

def decrypt(n, ciphertext):
    """Decrypt the string and return the plaintext"""
    result = ''

    for l in ciphertext:
        try:
            i = (SET_KEY.index(l) - n) % 26
            result += SET_KEY[i]
        except ValueError:
            result += l

    return result

# Set default batch count for presence.
def get_batch_count():
    return BATCH_COUNT

# Function to call AWS Facial Recognition
def get_aws_tags(image_url):
    session = boto3.Session()
    rekognition = session.client('rekognition')
    response = requests.get(image_url)
    response_content = response.content
    rekognition_response = rekognition.detect_faces(Image={'Bytes': response_content}, Attributes=['ALL'])
    try:
        get_face_details = rekognition_response['FaceDetails'][0]
        get_success = True
    except IndexError:
        get_success = False
        
        # Filtering tags required for UBS App
    if get_success:
        results = {
            'Code':1,
            'AgeRange':get_face_details['AgeRange'],
            'Smile':get_face_details['Smile'],
            'Eyeglasses':get_face_details['Eyeglasses'],
            'Sunglasses':get_face_details['Sunglasses'],
            'Gender':get_face_details['Gender'],
            'Beard':get_face_details['Beard'],
            'Mustache':get_face_details['Mustache'],
            'EyesOpen': get_face_details['EyesOpen'],
            'MouthOpen': get_face_details['MouthOpen'],
            'Emotions': get_face_details['Emotions']
            }
    else:
        results = {'Code':2, 'Error':'Invalid Image'}

    return results


def register_blueprints(app):
    from project.home import home_blueprint
    from project.profile import profile_blueprint
    from project.user import user_blueprint
    from project.presence import presence_blueprint
    from project.aws import aws_blueprint
    app.register_blueprint(home_blueprint)
    app.register_blueprint(profile_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(presence_blueprint)
    app.register_blueprint(aws_blueprint)
