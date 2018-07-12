from api import create_app
from api import db
from flask import current_app
from api.models.models import User, Menu, Orders, Meals
from werkzeug.security import generate_password_hash, check_password_hash
import unittest
import json

class auth_test_case(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.user_admin = {
            "fname": "toast",
            "lname": "bull",
            "email": "steven@gmail.com",
            "password": "54321",
            "role_id": 1,
            "business_name": "Fat Foods",
            "location": "Nakulabye"
        }
        self.user_normal = {
            "fname": "toast",
            "lname": "bull",
            "email": "tbull@gmail.com",
            "password": "12345",
            "role_id": 2
        }  

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_signup_missing_values(self):
        """ missing value in request sent"""
        user = {
            "fname": "brian",
            "lname": "Wagubi",
            "password": "12345"
        }
        response = self.client.post("/bookmealapi/v1.0/auth/signup",
                                    data=json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_signup_valid(self):
        """ valid json object, all fields avaiable """
        user = self.user_normal
        response = self.client.post("/bookmealapi/v1.0/auth/signup",
                                    data=json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'New user created!')
    
    def test_cannot_signup_same_email(self):
        """ cannot add item with same email again """
        user = self.user_normal
        response = self.client.post("/bookmealapi/v1.0/auth/signup",
                                    data=json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        user = user = self.user_normal
        response = self.client.post("/bookmealapi/v1.0/auth/signup",
                                    data=json.dumps(user), content_type='application/json')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], "Email Already Exists")

    def test_login_missing_values(self):
        """ missing values in json  """
        details = {
            "email": "wagubib@gmail.com"
        }
        response = self.client.post("/bookmealapi/v1.0/auth/login",
                                    data=json.dumps(details), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_login_valid_details_user(self):

        user = self.user_normal
        response = self.client.post("/bookmealapi/v1.0/auth/signup",
                                    data=json.dumps(user), content_type='application/json')

        """ correct details """
        details = {
            "email": "tbull@gmail.com",
            "password": "12345"
        }

        response = self.client.post("/bookmealapi/v1.0/auth/login",
                                    data=json.dumps(details), content_type='application/json')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], "Successfully login")

    def test_login_valid_details_admin(self):
        user = self.user_admin
        response = self.client.post("/bookmealapi/v1.0/auth/signup",
                                    data=json.dumps(user), content_type='application/json')

        """ correct details admin """
        details = {
            "email": "steven@gmail.com",
            "password": "54321"
        }
        response = self.client.post("/bookmealapi/v1.0/auth/login",
                                    data=json.dumps(details), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], "Successfully login")

    def test_login_invalid_password(self):
        """ Invalid Password """
        details = {
            "email": "lubega@gmail.com",
            "password": "54321"
        }
        response = self.client.post("/bookmealapi/v1.0/auth/login",
                                    data=json.dumps(details), content_type='application/json')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], "User Not Found")

    def test_login_invalid_username(self):
        """ invalid username """
        details = {
            "email": "fresh@gmail.com",
            "password": "12345"
        }
        response = self.client.post("/bookmealapi/v1.0/auth/login",
                                    data=json.dumps(details), content_type='application/json')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], "User Not Found")

