from flask import Flask, jsonify, request
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_claims)
from flasgger import Swagger, swag_from
from ..controllers.controller import EndpointFunctions

app = Flask(__name__)
swagger = Swagger(app)

app.config['JWT_SECRET_KEY'] = 'sentongo'
jwt = JWTManager(app)

endpoint_function = EndpointFunctions()

@app.route('/', methods=['GET'])
@swag_from('../apidocs/index.yml', methods=['GET'])
def home():
    return endpoint_function.home()

@app.route('/api/v2/messages', methods=['GET'])
@jwt_required
@swag_from('../apidocs/get_recieved.yml', methods=['GET'])
def all_recieved():
    return endpoint_function.select_email('none')

@app.route('/api/v2/messages/unread', methods=['GET'])
@jwt_required
@swag_from('../apidocs/get_unread.yml', methods=['GET'])
def all_unread():
    return endpoint_function.select_email('unread')

@app.route('/api/v2/messages/sent', methods=['GET'])
@jwt_required
@swag_from('../apidocs/get_sent.yml', methods=['GET'])
def all_sent():
    return endpoint_function.select_email('sent')
    
@app.route('/api/v2/messages/<int:mail_id>', methods=['GET'])
@jwt_required
@swag_from('../apidocs/get_specific.yml', methods=['GET'])
def specific(mail_id):
    return endpoint_function.select_email(mail_id)

@app.route('/api/v2/messages/<int:mail_id>', methods=['DELETE'])
@jwt_required
@swag_from('../apidocs/delete_email.yml', methods=['DELETE'])
def deletemail(mail_id):
    return endpoint_function.delete_email(mail_id)

@app.route('/api/v2/messages', methods=['POST'])
@jwt_required
@swag_from('../apidocs/send_email.yml', methods=['POST'])
def sendmail():
    return endpoint_function.send_email()

@app.route('/api/v2/auth/signup', methods=['POST'])
@swag_from('../apidocs/signup.yml', methods=['POST'])
def userSignup():
    return endpoint_function.create_account()

@app.route('/api/v2/auth/signin', methods=['POST'])
@swag_from('../apidocs/signin.yml', methods=['POST'])
def userSignin():
    return endpoint_function.signin()