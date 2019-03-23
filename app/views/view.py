from flask import Flask, jsonify, request
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_claims)
from ..controllers.controller import Endpoints_functions

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'sentongo'
jwt = JWTManager(app)

endpoint_function = Endpoints_functions()

@app.route('/', methods=['GET'])
def home():
    return endpoint_function.home()

@app.route('/api/v1/messages', methods=['GET'])
@jwt_required
def all_recieved():
    return endpoint_function.select_email('none')

@app.route('/api/v1/messages/unread', methods=['GET'])
def all_unread():
    return endpoint_function.select_email('unread')

@app.route('/api/v1/messages/sent', methods=['GET'])
@jwt_required
def all_sent():
    return endpoint_function.select_email('sent')
    
@app.route('/api/v1/messages/<int:email_id>', methods=['GET'])
@jwt_required
def specific(email_id):
    return endpoint_function.select_email(email_id)

@app.route('/api/v1/messages/<int:email_id>', methods=['DELETE'])
@jwt_required
def deletemail(email_id):
    return endpoint_function.delete_email(email_id)

@app.route('/api/v1/messages', methods=['POST'])
@jwt_required
def sendmail():
    return endpoint_function.send_email()

@app.route('/api/v1/auth/signup', methods=['POST'])
def userSignup():
    return endpoint_function.create_account()

@app.route('/api/v1/auth/signin', methods=['POST'])
def userSignin():
    return endpoint_function.signin()