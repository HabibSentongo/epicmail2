from datetime import datetime

mail_list = []

class mail:
    def __init__(self, **kwargs):
        self.mail_id = len(mail_list) + 1
        self.created_on = datetime.now()
        self.subject = kwargs.get("subject")
        self.parentMessageId = kwargs.get("parentMessageId")
        self.sen_status = kwargs.get("sen_status")
        self.rec_status = "unread"
        self.senderID = kwargs.get("senderID")
        self.recieverId = kwargs.get("recieverId")
        self.msgdetails = kwargs.get("msgdetails")

    def mail_struct(self, type):
        return {
            "mail_id": self.mail_id,
            "created_on": self.created_on,
            "subject": self.subject,
            "parentMessageId": self.parentMessageId,
            "sen_status": self.sen_status,
            "rec_status": self.rec_status,
            "senderID": self.senderID,
            "recieverId": self.recieverId,
            "msgdetails": self.msgdetails
        }

class Static_strings:
    error_empty = 'No records yet!'
    error_missing = 'No such record'
    error_bad_data = 'Provide correct details'
    error_no_id = 'We can\'t identify you, Signin first'
    msg_deleted = 'Record has been deleted'
    msg_updated = 'Updated record'