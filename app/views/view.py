from flask import Flask, jsonify, request
from ..controllers.controller import Endpoints_functions

app = Flask(__name__)
endpoint_function = Endpoints_functions()

@app.route('/', methods=['GET'])
def home():
    return endpoint_function.home()

@app.route('/api/v1/messages', methods=['GET'])
def all_recieved():
    return endpoint_function.mail_selector('none')

@app.route('/api/v1/messages/unread', methods=['GET'])
def all_unread():
    return endpoint_function.mail_selector('unread')

@app.route('/api/v1/messages/sent', methods=['GET'])
def all_sent():
    return endpoint_function.mail_selector('sent')
    
@app.route('/api/v1/messages/<int:mailID>', methods=['GET'])
def specific(mailID):
    return endpoint_function.mail_selector(mailID)

@app.route('/api/v1/messages/<int:mailID>', methods=['DELETE'])
def deletemail(mailID):
    return endpoint_function.mail_deletor(mailID)

@app.route('/api/v1/messages', methods=['POST'])
def sendmail():
    return endpoint_function.mail_send()

@app.route('/api/v1/auth/signup', methods=['POST'])
def userSignup():
    return endpoint_function.accreate()