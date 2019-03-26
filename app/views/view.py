from flask import Flask, jsonify, request
from ..controllers.controller import Endpoints_functions

app = Flask(__name__)
endpoint_function = Endpoints_functions()

@app.route('/')
def home():
    return endpoint_function.home()

@app.route('/api/v1/messages')
def all_recieved():
    return endpoint_function.mail_selector('none')

@app.route('/api/v1/messages/unread')
def all_unread():
    return endpoint_function.mail_selector('unread')

@app.route('/api/v1/messages/sent')
def all_sent():
    return endpoint_function.mail_selector('sent')
    