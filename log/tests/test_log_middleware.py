from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from log.log_middleware import LogMiddleware  # Adjust import path
from django.utils.encoding import force_bytes
import os

class MiddlewareTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def tearDown(self):
        if os.path.exists("log.txt"):
            os.remove("log.txt")

    def test_middleware_logs_request(self):
        user = User.objects.create_user(username='testuser', password='testpassword')

        request = self.factory.get('/test-url/')
        request.user = user
        request.headers = {'Content-Type': 'application/json'}
        request.GET = {'param1': 'value1', 'param2': 'value2'}
        request._body = force_bytes('{"key": "value"}')  # Use force_bytes to set the request body

        middleware = LogMiddleware(lambda req: None)

        middleware(request)

        with open("log.txt", "r") as f:
            logged_data = f.read()
            self.assertIn('"endpoint": "/test-url/"', logged_data)
            self.assertIn('"method": "GET"', logged_data)
            self.assertIn('"headers": {"Content-Type": "application/json"}', logged_data)
            self.assertIn('"query_params": {"param1": "value1", "param2": "value2"}', logged_data)
            self.assertIn('"user": "testuser"', logged_data)

        user.delete()

    def test_middleware_logs_request_without_user(self):
        if os.path.exists("log.txt"):
            os.remove("log.txt")

        request = self.factory.get('/test-url/')
        middleware = LogMiddleware(lambda req: None)
        middleware(request)

        with open("log.txt", "r") as f:
            logged_data = f.read()
            self.assertIn('"user": null', logged_data)

