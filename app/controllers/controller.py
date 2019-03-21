from flask import Flask, jsonify, request
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

    def mail_selector(self, key):
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
        if key == 'unread':
            for mail in mail_list:
                if mail['recieverId'] == current_Uid['user_id'] and mail['rec_status'] == key:
                    selected.append(mail)
        elif key == 'read':
            for mail in mail_list:
                if mail['recieverId'] == current_Uid['user_id'] and mail['rec_status'] == key:
                    selected.append(mail)
        elif key == 'sent':
            for mail in mail_list:
                if mail['senderID'] == current_Uid['user_id'] and mail['sen_status'] == key:
                    selected.append(mail)
        elif key == 'draft':
            for mail in mail_list:
                if mail['senderID'] == current_Uid['user_id'] and mail['sen_status'] == key:
                    selected.append(mail)
        elif key == 'none':
            for mail in mail_list:
                if mail['recieverId'] == current_Uid['user_id']:
                    selected.append(mail)
        else:
            for mail in mail_list:
                if mail['mail_id'] == key:
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

    def mail_deletor(self, key):
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
        for mail in mail_list:
                if mail['mail_id'] == key:
                    mail_list.remove(mail)
                    return jsonify({
                        'status': 200,
                        'data': [Static_strings.msg_deleted]
                    })
        return jsonify({
            'status': 204,
            'error': Static_strings.error_missing
        })

    def mail_send(self):
        if not request.json:
            return jsonify({
                'status': 417,
                'error': Static_strings.error_bad_data
            })
        mail_details = request.get_json()
        if 'senderID' not in mail_details:
            return jsonify({
                'status': 403,
                'error': Static_strings.error_no_id
            })
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
        senderID = mail_details.get("senderID")
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

    def accreate(self):
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
        return jsonify({
            'status': 201,
            'data': [
                new_user.user_struct()
            ]
        })