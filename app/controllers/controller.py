from flask import Flask, jsonify, request, json
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_claims, decode_token)
from ..models.mail_model import StaticStrings, mail_list, Mail
from ..models.user_model import user_list, User

class EndpointFunctions:
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
            selected = self.traverse('reciever_id','user_id', 'rec_status', key)
            
        elif key == 'read':
            selected = self.traverse('reciever_id','user_id', 'rec_status', key)

        elif key == 'sent':
            selected = self.traverse('sender_id','user_id', 'sen_status', key)
            
        elif key == 'draft':
            selected = self.traverse('sender_id','user_id', 'sen_status', key)

        elif key == 'none':
            selected = self.traverse('reciever_id','user_id', 'null', 'null')

        else:
            current_Uid = self.get_id_from_header_token()
            for mail in mail_list:
                if mail['mail_id'] == key and mail['reciever_id'] == current_Uid:
                    selected.append(mail)
                    mail['rec_status'] = 'read'
            if len(selected)==0:
                return jsonify({
                    'status': 404,
                    'error': StaticStrings.error_missing
                })

        if len(selected)>0:
            return jsonify({
                'status': 200,
                'data': selected
                })
        else:
            return jsonify({
                'status': 404,
                'error': StaticStrings.error_empty
            })

    def delete_email(self, key):
        current_Uid = self.get_id_from_header_token()
        for mail in mail_list:
                if mail['mail_id'] == key and (mail['sender_id'] == current_Uid or mail['reciever_id'] == current_Uid):
                    mail_list.remove(mail)
                    return jsonify({
                        'status': 200,
                        'data': [{
                            'message': StaticStrings.msg_deleted
                        }]
                    })
        return jsonify({
            'status': 404,
            'error': StaticStrings.error_missing
        })

    def send_email(self):
        mail_details = request.get_json()
        if not request.json or 'subject' not in mail_details:
            return jsonify({
                'status': 400,
                'error': StaticStrings.error_bad_data
            })
        if 'sen_status' not in mail_details:
            return jsonify({
                'status': 400,
                'error': StaticStrings.error_savemode
            })
        if mail_details['sen_status']=='sent' and 'reciever_id' not in mail_details:
            return jsonify({
                'status': 400,
                'error': StaticStrings.error_missdestination
            })
        
        subject = mail_details.get("subject")
        parent_message_id = mail_details.get("parent_message_id")
        sen_status = mail_details.get("sen_status")
        sender_id = self.get_id_from_header_token()
        reciever_id = mail_details.get("reciever_id")
        message_details = mail_details.get("message_details")

        new_mail = Mail(
            subject=subject,
            parent_message_id= parent_message_id,
            sen_status= sen_status,
            sender_id= sender_id,
            reciever_id= reciever_id,
            message_details= message_details
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
        user_details = request.get_json()
        if not request.json or 'email_address' not in user_details or 'first_name' not in user_details or 'last_name' not in user_details or 'password' not in user_details:
            return jsonify({
                'status': 400,
                'error': StaticStrings.error_bad_data
            })

        for user in user_list:
            if user['email_address'] == user_details['email_address']:
                return jsonify({
                'status': 400,
                'error': StaticStrings.error_email_exist
            })
        
        email_address = user_details.get("email_address")
        first_name = user_details.get("first_name")
        last_name = user_details.get("last_name")
        password = user_details.get("password")

        new_user = User(
            email_address=email_address,
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
        if not request.json or 'email_address' not in user_details or 'password' not in user_details:
            return jsonify({
                'status': 400,
                'error': StaticStrings.error_bad_data
            })
        
        email_address = user_details.get("email_address")
        password = user_details.get("password")

        for user in user_list:
            if user['email_address'] == email_address and user['password'] == password:
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