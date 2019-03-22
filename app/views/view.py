from flask import Flask, jsonify, request
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_claims)
from ..controllers.controller import Endpoints_functions

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'sentongo'
jwt = JWTManager(app)

endpoint_function = Endpoints_functions()

@jwt.user_claims_loader
def add_claims(identity):
    return {
        'current': identity
    }

@app.route('/', methods=['GET'])
def home():
    return endpoint_function.home()

@app.route('/api/v1/messages', methods=['GET'])
@jwt_required
def all_recieved():
    return endpoint_function.mail_selector('none')

@app.route('/api/v1/messages/unread', methods=['GET'])
@jwt_required
def all_unread():
    return endpoint_function.mail_selector('unread')

@app.route('/api/v1/messages/sent', methods=['GET'])
@jwt_required
def all_sent():
    return endpoint_function.mail_selector('sent')
    
@app.route('/api/v1/messages/<int:mailID>', methods=['GET'])
@jwt_required
def specific(mailID):
    return endpoint_function.mail_selector(mailID)

@app.route('/api/v1/messages/<int:mailID>', methods=['DELETE'])
@jwt_required
def deletemail(mailID):
    return endpoint_function.mail_deletor(mailID)

@app.route('/api/v1/messages', methods=['POST'])
@jwt_required
def sendmail():
    return endpoint_function.mail_send()

@app.route('/api/v1/auth/signup', methods=['POST'])
def userSignup():
    return endpoint_function.accreate()

@app.route('/api/v1/auth/signin', methods=['POST'])
def userSignin():
    return endpoint_function.signin()