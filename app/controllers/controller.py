from flask import Flask, jsonify, request
from ..models.incident_model import Static_strings

class Endpoints_functions:
    def home(self):
        return jsonify({'message': ['Welcome to Sentongo\'s EpicMail!',
                                    'Endpoints',
                                    '01 : POST /api/v1/auth/signup',
                                    '02 : POST /api/v1/auth/login',
                                    '03 : POST /api/v1/messages',
                                    '04 : GET /api/v1/messages',
                                    '05 : GET /api/v1/messages/unread',
                                    '06 : GET /api/v1/messages/sent',
                                    '07 : GET /api/v1/messages/<message-id>',
                                    '08 : DELETE /api/v1/messages/<message-id>']
                                        })