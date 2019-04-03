from flask import Flask, jsonify, request, json
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_claims, decode_token)
from database.db import DBmigrate
from ..models.mail_model import StaticStrings

db_obj = DBmigrate()
db_obj.create_tables()

class EndpointFunctions:
    def home(self):
        return jsonify({'status': 200,
                        'data': ['Welcome to Sentongo\'s EpicMail!',
                                'Endpoints',
                                '01 : POST /api/v2/auth/signup',
                                '02 : POST /api/v2/auth/login',
                                '03 : POST /api/v2/messages',
                                '04 : GET /api/v2/messages',
                                '05 : GET /api/v2/messages/unread',
                                '06 : GET /api/v2/messages/sent',
                                '07 : GET /api/v2/messages/<message-id>',
                                '08 : DELETE /api/v2/messages/<message-id>',
                                '09 : POST /api/v2/groups',
                                '10 : DELETE /api/v2/groups/<int:group_id>',
                                '11 : POST /api/v2/groups/<int:group_id>/users',
                                '12 : DELETE /api/v2/groups/<int:group_id>/users/<int:user_id>',
                                '13 : PATCH /api/v2/groups/<int:group_id>/name',
                                '14 : GET /api/v2/groups',
                                '15 : POST /api/v2/groups/<int:group_id>/messages',
                                '16 : POST /api/v2/auth/reset']
                                    })

    def get_id_from_header_token(self):
        header = request.headers.get('Authorization','')
        token = header.replace('Bearer ','')
        user_id = decode_token(token)['identity'] 
        return user_id

    def select_email(self, key):
        current_Uid = self.get_id_from_header_token()
        selected = []
        if key == 'unread':
            db_obj.my_cursor.execute(StaticStrings.selector.format('emails', 'reciever_id', current_Uid, 'reciever_status', key))
            selected = db_obj.my_cursor.fetchall()
            
        elif key == 'read':
            db_obj.my_cursor.execute(StaticStrings.selector.format('emails', 'reciever_id', current_Uid, 'reciever_status', key))
            selected = db_obj.my_cursor.fetchall()

        elif key == 'sent':
            db_obj.my_cursor.execute(StaticStrings.selector.format('emails', 'sender_id', current_Uid, 'sender_status', key))
            selected = db_obj.my_cursor.fetchall()

        elif key == 'draft':
            db_obj.my_cursor.execute(StaticStrings.selector.format('emails', 'sender_id', current_Uid, 'sender_status', key))
            selected = db_obj.my_cursor.fetchall()

        elif key == 'none':
            db_obj.my_cursor.execute(StaticStrings.selector.format('emails', 'reciever_id', current_Uid, 'sender_status', 'sent'))
            selected = db_obj.my_cursor.fetchall()

        else:
            db_obj.my_cursor.execute(StaticStrings.selector.format('emails', 'reciever_id', current_Uid, 'mail_id', key))
            selected = db_obj.my_cursor.fetchall()
            if len(selected)==0:
                return jsonify({
                    'status': 404,
                    'error': StaticStrings.error_missing
                })
            db_obj.my_cursor.execute(StaticStrings.updater.format('emails' ,'reciever_status', 'read', 'mail_id', key))

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
        db_obj.my_cursor.execute(StaticStrings.two_id_selector.format('emails','mail_id',key,'reciever_id',current_Uid,'sender_id',current_Uid))
        data = db_obj.my_cursor.fetchall()
        if len(data)>0:
            db_obj.my_cursor.execute(StaticStrings.deleter.format('emails' , 'mail_id', key))
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

    def send_email(self, recipient_table):
        current_Uid = self.get_id_from_header_token()
        mail_details = request.get_json()
        if not request.json or 'subject' not in mail_details:
            return jsonify({
                'status': 400,
                'error': StaticStrings.error_bad_data
            })
        if 'sender_status' not in mail_details:
            return jsonify({
                'status': 400,
                'error': StaticStrings.error_savemode
            })

        if 'reciever_email' not in mail_details:
            return jsonify({
                'status': 400,
                'error': StaticStrings.error_missdestination
            })

        reciever_email = mail_details.get("reciever_email")
        db_obj.my_cursor.execute(StaticStrings.id_selector.format(reciever_email))
        data = db_obj.my_cursor.fetchall()
        if len(data)<0:
            return jsonify({
                'status': 404,
                'error': StaticStrings.error_missdestination
            })

        subject = mail_details.get("subject")
        parent_message_id = mail_details.get("parent_message_id")
        sender_status = mail_details.get("sender_status")
        reciever_status = ''
        if sender_status == 'sent':
            reciever_status = 'unread'
        sender_id = current_Uid
        reciever_id = data[0]['user_id']
        message_details = mail_details.get("message_details")

        db_obj.my_cursor.execute(StaticStrings.create_email.format(recipient_table,subject, parent_message_id, sender_status, sender_id, reciever_id, reciever_status, message_details))
        new_mail = db_obj.my_cursor.fetchall()
        return jsonify({
            'status': 201,
            'data': new_mail
        })

    def create_account(self):
        user_details = request.get_json()
        if not request.json or 'email_address' not in user_details or 'first_name' not in user_details or 'last_name' not in user_details or 'password' not in user_details:
            return jsonify({
                'status': 400,
                'error': StaticStrings.error_bad_data
            })

        email_address = user_details.get("email_address")
        first_name = user_details.get("first_name")
        last_name = user_details.get("last_name")
        password = user_details.get("password")

        db_obj.my_cursor.execute(StaticStrings.single_selector.format('users', 'email_address', email_address))
        data = db_obj.my_cursor.fetchall()
        if data:
            return jsonify({
                'status': 400,
                'error': StaticStrings.error_email_exist
            })
        
        db_obj.my_cursor.execute(StaticStrings.create_user.format(email_address,first_name, last_name, password))
        user_id = db_obj.my_cursor.fetchall()[0]['user_id']
        token = create_access_token(user_id)
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

        db_obj.my_cursor.execute(StaticStrings.two_string_selector.format('users','email_address',email_address,'password',password))
        data = db_obj.my_cursor.fetchall()
        if data:
            currentID = data[0]['user_id']
            token = create_access_token(currentID)
            return jsonify({
                'status': 200,
                'data': [{
                    'token': token
                }]
            })
        return jsonify({
                    'status': 404,
                    'error': 'Wrong email and/or password'
                })

    def create_group(self):
        current_Uid = self.get_id_from_header_token()
        group_details = request.get_json()
        if not request.json or 'group_name' not in group_details:
            return jsonify({
                'status': 400,
                'error': StaticStrings.error_bad_data
            })
        
        group_name = group_details.get("group_name")
        admin = current_Uid
        members = [current_Uid]
        
        db_obj.my_cursor.execute(StaticStrings.create_group.format(group_name, admin, members))
        new_group = db_obj.my_cursor.fetchall()
        return jsonify({
            'status': 201,
            'data': new_group
        })

    def delete_group(self, key):
        current_Uid = self.get_id_from_header_token()
        db_obj.my_cursor.execute(StaticStrings.two_id_selector.format('groups','group_id',key,'admin',current_Uid,'admin',current_Uid))
        data = db_obj.my_cursor.fetchall()
        if len(data)>0:
            db_obj.my_cursor.execute(StaticStrings.deleter.format('groups' , 'group_id', key))
            return jsonify({
                'status': 200,
                'data': [{
                    'message': StaticStrings.msg_deleted
                }]
            })
        return jsonify({
            'status': 401,
            'error': StaticStrings.not_allowed
        })

    def add_member(self, key):
        current_Uid = self.get_id_from_header_token()
        user = request.get_json()
        if not request.json or 'user_id' not in user:
            return jsonify({
                'status': 400,
                'error': StaticStrings.error_bad_data
            })
        
        user_id = user.get("user_id")
        db_obj.my_cursor.execute(StaticStrings.two_id_selector.format('groups','group_id',key,'admin',current_Uid,'admin',current_Uid))
        data = db_obj.my_cursor.fetchall()
        if len(data)>0:
            if user_id not in data[0]['members']:
                members = data[0]['members']
                members.append(user_id)
                db_obj.my_cursor.execute(StaticStrings.update_members.format(members , key))
                data = db_obj.my_cursor.fetchall()
                return jsonify({
                    'status': 200,
                    'data': [{
                        'message': 'User Succesfully added',
                        'group_details': data[0]
                    }]
                })
            return jsonify({
                    'status': 400,
                    'data': [{
                        'message': 'User already in this group'
                    }]
                })
        return jsonify({
            'status': 401,
            'error': StaticStrings.not_allowed
        })

    def delete_member(self, key, member):
        current_Uid = self.get_id_from_header_token()
        db_obj.my_cursor.execute(StaticStrings.two_id_selector.format('groups','group_id',key,'admin',current_Uid,'admin',current_Uid))
        data = db_obj.my_cursor.fetchall()
        if len(data)>0:
            if member in data[0]['members'] and member != current_Uid:
                members = data[0]['members']
                members.remove(member)
                db_obj.my_cursor.execute(StaticStrings.update_members.format(members, key))
                data = db_obj.my_cursor.fetchall()
                return jsonify({
                    'status': 200,
                    'data': [{
                        'message': 'User Succesfully removed',
                        'group_details': data[0]
                    }]
                })
            if member == current_Uid:
                return jsonify({
                    'status': 400,
                    'data': [{
                        'message': 'Admin cannot be deleted from group'
                    }]
                })
            return jsonify({
                    'status': 400,
                    'data': [{
                        'message': 'No such user in this group'
                    }]
                })
        return jsonify({
            'status': 401,
            'error': StaticStrings.not_allowed
        })

    def rename_group(self, group_id):
        current_Uid = self.get_id_from_header_token()
        info = request.get_json()
        if not request.json or 'new_name' not in info:
            return jsonify({
                'status': 400,
                'error': StaticStrings.error_bad_data
            })
        new_name = info.get("new_name")
        db_obj.my_cursor.execute(StaticStrings.two_id_selector.format('groups','group_id',group_id,'admin',current_Uid,'admin',current_Uid))
        data = db_obj.my_cursor.fetchall()
        if len(data)>0:
            db_obj.my_cursor.execute(StaticStrings.updater.format('groups','group_name',new_name,'group_id',group_id))
            data = db_obj.my_cursor.fetchall()
            return jsonify({
                'status': 200,
                'data': [{
                    'message': 'Group successfuly renamed',
                    'group_details': data[0]
                }]
            })
        return jsonify({
            'status': 401,
            'error': StaticStrings.not_allowed
        })

    def all_groups(self):
        currentID = self.get_id_from_header_token()
        db_obj.my_cursor.execute(StaticStrings.select_all.format('groups'))
        all_groups = db_obj.my_cursor.fetchall()
        selected = []
        for group in all_groups:
            if currentID in group['members']:
                selected.append(group)
        if len(selected)>0:
            return jsonify({
                'status': 200,
                'data': selected
            })
        return jsonify({
                'status': 404,
                'error': 'You are not in any group!'
            })

    def send_grp_email(self, recipient_table,group_id):
        current_Uid = self.get_id_from_header_token()
        mail_details = request.get_json()
        if not request.json or 'subject' not in mail_details:
            return jsonify({
                'status': 400,
                'error': StaticStrings.error_bad_data
            })
        if 'sender_status' not in mail_details:
            return jsonify({
                'status': 400,
                'error': StaticStrings.error_savemode
            })

        if 'reciever_id' not in mail_details:
            return jsonify({
                'status': 400,
                'error': StaticStrings.error_missdestination
            })
        
        subject = mail_details.get("subject")
        parent_message_id = mail_details.get("parent_message_id")
        sender_status = mail_details.get("sender_status")
        reciever_status = ''
        if sender_status == 'sent':
            reciever_status = 'unread'
        sender_id = current_Uid
        reciever_id = group_id
        message_details = mail_details.get("message_details")

        db_obj.my_cursor.execute(StaticStrings.create_email.format(recipient_table,subject, parent_message_id, sender_status, sender_id, reciever_id, reciever_status, message_details))
        new_mail = db_obj.my_cursor.fetchall()
        return jsonify({
            'status': 201,
            'data': new_mail
        })

    def send_group_email(self, group_id):
        current_Uid = self.get_id_from_header_token()
        db_obj.my_cursor.execute(StaticStrings.single_id_selector.format('*','groups','group_id',group_id))
        data = db_obj.my_cursor.fetchall()
        if data:
            if current_Uid in data[0]['members']:
                result = self.send_grp_email('group_emails',group_id)
                return result
            return jsonify({
                    'status': 400,
                    'data': [{
                        'message': 'You are not a member of this group'
                    }]
                })
        return jsonify({
            'status': 404,
            'error': StaticStrings.error_missing
        })

    def forgot_password(self):
        user = request.get_json()
        if not request.json or 'email_address' not in user or 'new_password' not in user:
            return jsonify({
                'status': 400,
                'error': StaticStrings.error_bad_data
            })
        
        email_address = user.get("email_address")
        new_password = user.get('new_password')
        db_obj.my_cursor.execute(StaticStrings.single_selector.format('users','email_address',email_address))
        data = db_obj.my_cursor.fetchall()
        if len(data)>0:
            user_id = data[0]['user_id']
            db_obj.my_cursor.execute(StaticStrings.updater.format('users','password',new_password,'user_id',user_id))
            data = db_obj.my_cursor.fetchall()
            return jsonify({
                'status': 200,
                'data': [{
                    'message': 'User password Succesfully updated',
                    'new_details': data[0]
                }]
            })
        return jsonify({
            'status': 404,
            'error': StaticStrings.error_missing
        })