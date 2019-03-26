import unittest
from app.views.view import app
import json

class TestApi(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()

    def tearDown(self):
        pass

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