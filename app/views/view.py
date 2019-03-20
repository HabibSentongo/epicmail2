from flask import Flask, jsonify, request
from ..controllers.controller import Endpoints_functions

app = Flask(__name__)
endpoint_function = Endpoints_functions()

@app.route('/')
def home():
    return endpoint_function.home()