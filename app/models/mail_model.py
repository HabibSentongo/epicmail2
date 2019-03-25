from datetime import datetime

mail_list = []

class Mail:
    def __init__(self, **kwargs):
        self.mail_id = len(mail_list) + 1
        self.created_on = datetime.now()
        self.subject = kwargs.get("subject")
        self.parent_message_id = kwargs.get("parent_message_id")
        self.sen_status = kwargs.get("sen_status")
        self.rec_status = "unread"
        self.sender_id = kwargs.get("sender_id")
        self.reciever_id = kwargs.get("reciever_id")
        self.message_details = kwargs.get("message_details")

    def mail_struct(self):
        return {
            "mail_id": self.mail_id,
            "created_on": self.created_on,
            "subject": self.subject,
            "parent_message_id": self.parent_message_id,
            "sen_status": self.sen_status,
            "rec_status": self.rec_status,
            "sender_id": self.sender_id,
            "reciever_id": self.reciever_id,
            "message_details": self.message_details
        }

class StaticStrings:
    error_empty = 'No records yet!'
    error_missing = 'No such record'
    error_bad_data = 'Provide correct details'
    error_no_id = 'We can\'t identify you, Signin first'
    msg_deleted = 'Record has been deleted'
    error_savemode = 'You must send the email or save it as draft'
    error_missdestination = 'destination address is missing'
    error_email_exist = 'This email is already associated with another account'