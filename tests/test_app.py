import unittest
from app.views.view import app
from app.models.mail_model import Static_strings, mail_list
from app.models.user_model import user_list
import json

class TestApi(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()

    def tearDown(self):
        user_list[:] = []
        mail_list[:] = []

    def helper_fn(self, what, to_who):
        if what == 'signup':
            token = json.loads(self.client.post('/api/v1/auth/signup', data = json.dumps({
            "email_add": "habib@sentongo.andela",
            "first_name": "Habib",
            "last_name": "Sentongo",
            "password": "andela"
            }),content_type = 'application/json').data.decode())['data'][0]['token']
            return token
        if what == 'send_email':
            token = json.loads(self.client.post('/api/v1/auth/signup', data = json.dumps({
            "email_add": "habib@sentongo.andela",
            "first_name": "Habib",
            "last_name": "Sentongo",
            "password": "andela"
            }),content_type = 'application/json').data.decode())['data'][0]['token']

            self.client.post('/api/v1/messages', data = json.dumps({
            "subject": "how cool",
            "parentMessageId": 4,
            "sen_status": "sent",
            "recieverId": to_who,
            "msgdetails": "sentongo is cool wen u cool"
            }),content_type = 'application/json', headers = dict(Authorization = 'Bearer '+ token))
            return token

    def test_home_status(self):
        response = self.client.get('/', content_type = 'application/json')
        self.assertEqual(response.status_code, 200)
        returndata = json.loads(response.data.decode())
        expected = ['Welcome to Sentongo\'s EpicMail!',
                    'Endpoints',
                    '01 : POST /api/v1/auth/signup',
                    '02 : POST /api/v1/auth/login',
                    '03 : POST /api/v1/messages',
                    '04 : GET /api/v1/messages',
                    '05 : GET /api/v1/messages/unread',
                    '06 : GET /api/v1/messages/sent',
                    '07 : GET /api/v1/messages/<message-id>',
                    '08 : DELETE /api/v1/messages/<message-id>']
        self.assertEqual(returndata['data'], expected)

    def test_signup_without_post_data(self):
        response = json.loads(self.client.post('/api/v1/auth/signup',data = json.dumps({}), content_type = 'application/json').data.decode())
        self.assertEqual(response['status'],400)
        self.assertEqual(response['error'], Static_strings.error_bad_data)

    def test_signup_without_email(self):
        response = json.loads(self.client.post('/api/v1/auth/signup', data = json.dumps({
            "first_name": "Habib",
            "last_name": "Sentongo",
            "password": "andela"
        }),content_type = 'application/json').data.decode())
        self.assertEqual(response['status'],400)
        self.assertEqual(response['error'], Static_strings.error_bad_data)

    def test_signup_good_request(self):
        response = json.loads(self.client.post('/api/v1/auth/signup', data = json.dumps({
            "email_add": "habib@sentongo.andela",
            "first_name": "Habib",
            "last_name": "Sentongo",
            "password": "andela"
        }),content_type = 'application/json').data.decode())
        self.assertEqual(response['status'],201)
        self.assertEqual(type(response['data'][0]['token']), type(''))

    def test_signin_without_post_data(self):
        response = json.loads(self.client.post('/api/v1/auth/signin',data = json.dumps({}), content_type = 'application/json').data.decode())
        self.assertEqual(response['status'],400)
        self.assertEqual(response['error'], Static_strings.error_bad_data)

    def test_signin_with_wrong_credentials(self):
        self.client.post('/api/v1/auth/signup', data = json.dumps({
            "email_add": "habib@sentongo.andela",
            "first_name": "Habib",
            "last_name": "Sentongo",
            "password": "andela"
        }),content_type = 'application/json')
        response = json.loads(self.client.post('/api/v1/auth/signin', data = json.dumps({
            "email_add": "b@sentongo.andela",
            "password": "andela"
        }),content_type = 'application/json').data.decode())
        self.assertEqual(response['status'],404)
        self.assertEqual(response['error'], 'Bad email and/or password')

    def test_signin_good_request(self):
        self.client.post('/api/v1/auth/signup', data = json.dumps({
            "email_add": "habib@sentongo.andela",
            "first_name": "Habib",
            "last_name": "Sentongo",
            "password": "andela"
        }),content_type = 'application/json')
        response = json.loads(self.client.post('/api/v1/auth/signin', data = json.dumps({
            "email_add": "habib@sentongo.andela",
            "password": "andela"
        }),content_type = 'application/json').data.decode())
        self.assertEqual(response['status'],200)
        self.assertEqual(type(response['data'][0]['token']), type(''))

    def test_send_email_good_request(self):
        token = self.helper_fn('signup', '')
        response = json.loads(self.client.post('/api/v1/messages', data = json.dumps({
            "subject": "how cool",
            "parentMessageId": 4,
            "sen_status": "sent",
            "recieverId": 2,
            "msgdetails": "sentongo is cool wen u cool"
        }),content_type = 'application/json', headers = dict(Authorization = 'Bearer '+ token)).data.decode())
        self.assertEqual(response['status'],201)
        self.assertEqual(response['data'][0]['msgdetails'], 'sentongo is cool wen u cool')

    def test_send_email_missing_recipient(self):
        token = self.helper_fn('signup', '')
        response = json.loads(self.client.post('/api/v1/messages', data = json.dumps({
            "subject": "how cool",
            "parentMessageId": 4,
            "sen_status": "sent",
            "msgdetails": "sentongo is cool wen u cool"
        }),content_type = 'application/json', headers = dict(Authorization = 'Bearer '+ token)).data.decode())
        self.assertEqual(response['status'],400)
        self.assertEqual(response['error'], Static_strings.error_missdestination)

    def test_send_email_missing_status(self):
        token = self.helper_fn('signup', '')
        response = json.loads(self.client.post('/api/v1/messages', data = json.dumps({
            "subject": "how cool",
            "parentMessageId": 4,
            "recieverId": 1,
            "msgdetails": "sentongo is cool wen u cool"
        }),content_type = 'application/json', headers = dict(Authorization = 'Bearer '+ token)).data.decode())
        self.assertEqual(response['status'],400)
        self.assertEqual(response['error'], Static_strings.error_savemode)

    def test_send_email_no_request_data(self):
        token = self.helper_fn('signup', '')
        response = json.loads(self.client.post('/api/v1/messages', data = json.dumps({}),content_type = 'application/json', headers = dict(Authorization = 'Bearer '+ token)).data.decode())
        self.assertEqual(response['status'],400)
        self.assertEqual(response['error'], Static_strings.error_bad_data)

    def test_delete_email_that_doesnt_exist(self):
        token = self.helper_fn('signup', '')
        response = json.loads(self.client.delete('/api/v1/messages/2', data = json.dumps({}),content_type = 'application/json', headers = dict(Authorization = 'Bearer '+ token)).data.decode())
        self.assertEqual(response['status'],404)
        self.assertEqual(response['error'], Static_strings.error_missing)

    def test_delete_email_good_request(self):
        token = self.helper_fn('signup', '')
        self.helper_fn('send_email', 1)
        response = json.loads(self.client.delete('/api/v1/messages/1', data = json.dumps({}),content_type = 'application/json', headers = dict(Authorization = 'Bearer '+ token)).data.decode())
        self.assertEqual(response['status'],200)
        self.assertEqual(response['data'][0]['message'], Static_strings.msg_deleted)

    def test_get_all_good_request(self):
        token = self.helper_fn('signup', '')
        self.helper_fn('send_email', 1)
        response = json.loads(self.client.get('/api/v1/messages', data = json.dumps({}),content_type = 'application/json', headers = dict(Authorization = 'Bearer '+ token)).data.decode())
        self.assertEqual(response['status'],200)
        self.assertEqual(len(response['data']), 1)

    def test_get_unread_good_request(self):
        token = self.helper_fn('signup', '')
        self.helper_fn('send_email', 1)
        response = json.loads(self.client.get('/api/v1/messages/unread', data = json.dumps({}),content_type = 'application/json', headers = dict(Authorization = 'Bearer '+ token)).data.decode())
        self.assertEqual(response['status'],200)
        self.assertEqual(len(response['data']), 1)
         
    def test_get_specific_good_request(self):
        token = self.helper_fn('signup', '')
        self.helper_fn('send_email', 1)
        response = json.loads(self.client.get('/api/v1/messages/1', data = json.dumps({}),content_type = 'application/json', headers = dict(Authorization = 'Bearer '+ token)).data.decode())
        self.assertEqual(response['status'],200)
        self.assertEqual(len(response['data']), 1)

    def test_get_sent_good_request(self):
        token = self.helper_fn('send_email', 1)
        response = json.loads(self.client.get('/api/v1/messages/sent', data = json.dumps({}),content_type = 'application/json', headers = dict(Authorization = 'Bearer '+ token)).data.decode())
        self.assertEqual(response['status'],200)
        self.assertEqual(len(response['data']), 1)