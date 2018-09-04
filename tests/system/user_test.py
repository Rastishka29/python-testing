from models.user import UserModel
from tests.test_base import BaseTest
import json


class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:  # enabling us to make requests to the api
            with self.app_context():  # enabling us to save and retrieve data to/from the db
                response = client.post('/register', data={'username': 'test', 'password': 'felix'})

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('test'))
                self.assertDictEqual(json.loads(response.data), {'message': 'Successfully created'})

    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': 'test', 'password': 'felix'})
                auth_response = client.post('/auth',
                                            data=json.dumps({'username': 'test', 'password': 'felix'}),
                                            headers={'Content-type': 'Application/json'})

                self.assertIn('access_token', json.loads(auth_response.data).keys())  # ['access_token']

    def test_register_existing_user(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': 'test', 'password': 'felix'})
                response = client.post('/register', data={'username': 'test', 'password': 'felix'})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual(json.loads(response.data),
                                     {'message': 'A user with such username already exists'})
