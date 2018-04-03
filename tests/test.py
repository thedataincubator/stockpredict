import unittest
import requests
import responses
from stockticker import create_app

class TestApp(unittest.TestCase):

    def setUp(self):
        self.url = 'http://a_url'
        self.secret_key = 'a'
        app = create_app(self.url, self.secret_key)
        app.testing = True
        self.app = app.test_client()

    @responses.activate
    def test_post_error(self):
        responses.add(responses.POST, self.url,
                      json={'error': 'not found'}, 
                      status=404)
        res = self.app.get('/')
        self.assertEqual(res.status_code, 404)

    @responses.activate
    def test_post_success(self):
        responses.add(responses.POST, self.url,
                      json={'ds': [1,2,3,4],
                            'yhat': [2,3,4,5]},
                      status=200)
        res = self.app.get('/')
        self.assertEqual(res.status_code, 200)
