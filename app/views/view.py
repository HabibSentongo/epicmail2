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
def delete_mail(mail_id):
    return endpoint_function.delete_email(mail_id)

@app.route('/api/v2/messages', methods=['POST'])
@jwt_required
@swag_from('../apidocs/send_email.yml', methods=['POST'])
def send_mail():
    return endpoint_function.send_email('emails')

@app.route('/api/v2/auth/signup', methods=['POST'])
@swag_from('../apidocs/signup.yml', methods=['POST'])
def user_signup():
    return endpoint_function.create_account()

@app.route('/api/v2/auth/signin', methods=['POST'])
@swag_from('../apidocs/signin.yml', methods=['POST'])
def user_signin():
    return endpoint_function.signin()

@app.route('/api/v2/groups', methods=['POST'])
@jwt_required
@swag_from('../apidocs/send_email.yml', methods=['POST'])
def create_group():
    return endpoint_function.create_group()

@app.route('/api/v2/groups/<int:group_id>', methods=['DELETE'])
@jwt_required
@swag_from('../apidocs/delete_email.yml', methods=['DELETE'])
def delete_group(group_id):
    return endpoint_function.delete_group(group_id)

@app.route('/api/v2/groups/<int:group_id>/users', methods=['POST'])
@jwt_required
@swag_from('../apidocs/send_email.yml', methods=['POST'])
def add_member(group_id):
    return endpoint_function.add_member(group_id)

@app.route('/api/v2/groups/<int:group_id>/users/<int:user_id>', methods=['DELETE'])
@jwt_required
@swag_from('../apidocs/send_email.yml', methods=['DELETE'])
def delete_member(group_id, user_id):
    return endpoint_function.delete_member(group_id, user_id)

@app.route('/api/v2/groups/<int:group_id>/messages', methods=['POST'])
@jwt_required
@swag_from('../apidocs/send_email.yml', methods=['POST'])
def send_group_mail(group_id):
    return endpoint_function.send_group_email(group_id)

@app.route('/api/v2/auth/reset', methods=['POST'])
@swag_from('../apidocs/send_email.yml', methods=['POST'])
def reset_password():
    return endpoint_function.forgot_password()