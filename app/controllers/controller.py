from flask import Flask, jsonify, request
from ..models.mail_model import Static_strings, mail_list

class Endpoints_functions:
    def home(self):
        return jsonify({'status': 200,
                        'data': ['Welcome to Sentongo\'s EpicMail!',
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

    def all_recieved(self):
        if not request.json:
            return jsonify({
                'status': 417,
                'error': Static_strings.error_no_id
            })
        current_Uid = request.get_json()
        if 'user_id' not in current_Uid:
            return jsonify({
                'status': 417,
                'error': Static_strings.error_no_id
            })
        selected = []
        for mail in mail_list:
            if mail['recieverId'] == current_Uid['user_id']:
                selected.append(mail)
        if len(selected)>0:
            return jsonify({
                'status': 302,
                'data': selected
                })
        else:
            return jsonify({
                'status': 204,
                'error': Static_strings.error_empty
            })

    def all_unread(self):
        if not request.json:
            return jsonify({
                'status': 417,
                'error': Static_strings.error_no_id
            })
        current_Uid = request.get_json()
        if 'user_id' not in current_Uid:
            return jsonify({
                'status': 417,
                'error': Static_strings.error_no_id
            })
        selected = []
        for mail in mail_list:
            if mail['recieverId'] == current_Uid['user_id'] and mail['rec_status'] == 'unread':
                selected.append(mail)
        if len(selected)>0:
            return jsonify({
                'status': 302,
                'data': selected
                })
        else:
            return jsonify({
                'status': 204,
                'error': Static_strings.error_empty
            })