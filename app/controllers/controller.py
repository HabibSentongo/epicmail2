from flask import Flask, jsonify, request, json
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_claims, decode_token)
from ..models.mail_model import Static_strings, mail_list, Mail
from ..models.user_model import user_list, User

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

    def get_id_from_header_token(self):
        header = request.headers.get('Authorization','')
        token = header.replace('Bearer ','')
        if not token:
            return jsonify({
                'status': 471,
                'error': Static_strings.error_no_id
            })
        user_id = decode_token(token)['identity'] 
        return user_id


    def traverse(self, user_id, current_id, criteria, key):
        current_Uid = self.get_id_from_header_token()
        selected = []
        for mail in mail_list:
            if criteria == 'null' and key == 'null':
                if mail[user_id] == current_Uid:
                    selected.append(mail)

            if mail[user_id] == current_Uid and mail.get(criteria) == key:
                selected.append(mail)
        return selected

    def select_email(self, key):
        selected = []
        if key == 'unread':
            selected = self.traverse('recieverId','user_id', 'rec_status', key)
            
        elif key == 'read':
            selected = self.traverse('recieverId','user_id', 'rec_status', key)

        elif key == 'sent':
            selected = self.traverse('senderID','user_id', 'sen_status', key)
            
        elif key == 'draft':
            selected = self.traverse('senderID','user_id', 'sen_status', key)

        elif key == 'none':
            selected = self.traverse('recieverId','user_id', 'null', 'null')

        else:
            current_Uid = self.get_id_from_header_token()
            for mail in mail_list:
                if mail['mail_id'] == key and mail['recieverId'] == current_Uid:
                    selected.append(mail)
            if len(selected)==0:
                return jsonify({
                    'status': 204,
                    'error': Static_strings.error_missing
                })

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

    def delete_email(self, key):
        current_Uid = self.get_id_from_header_token()
        for mail in mail_list:
                if mail['mail_id'] == key and (mail['senderID'] == current_Uid or mail['recieverId'] == current_Uid):
                    mail_list.remove(mail)
                    return jsonify({
                        'status': 200,
                        'data': [{
                            'message': Static_strings.msg_deleted
                        }]
                    })
        return jsonify({
            'status': 204,
            'error': Static_strings.error_missing
        })

    def send_email(self):
        if not request.json:
            return jsonify({
                'status': 417,
                'error': Static_strings.error_bad_data
            })
        mail_details = request.get_json()
        if 'sen_status' not in mail_details:
            return jsonify({
                'status': 417,
                'error': Static_strings.error_savemode
            })
        if mail_details['sen_status']=='sent' and 'recieverId' not in mail_details:
            return jsonify({
                'status': 417,
                'error': Static_strings.error_missdestination
            })
        
        subject = mail_details.get("subject")
        parentMessageId = mail_details.get("parentMessageId")
        sen_status = mail_details.get("sen_status")
        senderID = self.get_id_from_header_token()
        recieverId = mail_details.get("recieverId")
        msgdetails = mail_details.get("msgdetails")

        new_mail = Mail(
            subject=subject,
            parentMessageId= parentMessageId,
            sen_status= sen_status,
            senderID= senderID,
            recieverId= recieverId,
            msgdetails= msgdetails
        )

        mail_list.append(
            new_mail.mail_struct()
        )
        return jsonify({
            'status': 201,
            'data': [
                new_mail.mail_struct()
            ]
        })

    def create_account(self):
        if not request.json:
            return jsonify({
                'status': 417,
                'error': Static_strings.error_bad_data
            })
        user_details = request.get_json()
        if 'email_add' not in user_details or 'first_name' not in user_details or 'last_name' not in user_details or 'password' not in user_details:
            return jsonify({
                'status': 403,
                'error': Static_strings.error_bad_data
            })
        
        email_add = user_details.get("email_add")
        first_name = user_details.get("first_name")
        last_name = user_details.get("last_name")
        password = user_details.get("password")

        new_user = User(
            email_add=email_add,
            first_name= first_name,
            last_name= last_name,
            password= password
        )

        user_list.append(
            new_user.user_struct()
        )
        token = create_access_token(new_user.user_struct()['user_id'])
        return jsonify({
                    'status': 201,
                    'data': [{
                        'token': token
                    }]
                })
    def signin(self):
        user_details = request.get_json()
        if not request.json or 'email_add' not in user_details or 'password' not in user_details:
            return jsonify({
                'status': 417,
                'error': Static_strings.error_bad_data
            })
        
        email_add = user_details.get("email_add")
        password = user_details.get("password")

        for user in user_list:
            if user['email_add'] == email_add and user['password'] == password:
                currentID = user['user_id']
                token = create_access_token(currentID)
                return jsonify({
                    'status': 200,
                    'data': [{
                        'token': token
                    }]
                })
        return jsonify({
                    'status': 404,
                    'error': 'Bad email and/or password'
                })