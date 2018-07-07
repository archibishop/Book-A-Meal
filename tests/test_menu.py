from api import create_app
from api import db
from flask import current_app
from api.models.models import User
from api.models.models import Menu
from api.models.models import Orders
from api.models.models import Meals
from werkzeug.security import generate_password_hash, check_password_hash
import unittest
import json


class meal_test_case(unittest.TestCase):
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
        self.login_admin = {
            "email": "steven@gmail.com",
            "password": "54321"
        }
        self.valid_menu = {
            "meal_ids": [1, 2, 3, 4],
            "user_id": 1
        }

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_set_menu(self):
        """ setting the menu """
        user = self.user_admin
        response = self.client.post("/bookmealapi/v1.0/auth/signup",
                                    data=json.dumps(user), content_type='application/json')

        """ correct details admin """
        details = self.login_admin
        response = self.client.post("/bookmealapi/v1.0/auth/login",
                                    data=json.dumps(details), content_type='application/json')
        data = json.loads(response.get_data())
        token = data['token']

        details = self.valid_menu
        response = self.client.post("/bookmealapi/v1.0/menu",
                                    data=json.dumps(details), content_type='application/json',
                                    headers={'x-access-token': token})
        self.assertEqual(response.status_code, 201)

    def test_update_menu_missing_value(self):
        """ Incomplete json sent """
        user = self.user_admin
        response = self.client.post("/bookmealapi/v1.0/auth/signup",
                                    data=json.dumps(user), content_type='application/json')

        details = self.login_admin
        response = self.client.post("/bookmealapi/v1.0/auth/login",
                                    data=json.dumps(details), content_type='application/json')
        data = json.loads(response.get_data())
        token = data['token']

        details = {
            "user_id": 3
        }
        response = self.client.put("/bookmealapi/v1.0/menu/1",
                                   data=json.dumps(details), content_type='application/json',
                                   headers={'x-access-token': token})
        self.assertEqual(response.status_code, 400)

    def test_update_menu_nonexistant(self):
        """ Incomplete json sent """
        user = self.user_admin
        response = self.client.post("/bookmealapi/v1.0/auth/signup",
                                    data=json.dumps(user), content_type='application/json')

        details = self.login_admin
        response = self.client.post("/bookmealapi/v1.0/auth/login",
                                    data=json.dumps(details), content_type='application/json')
        data = json.loads(response.get_data())
        token = data['token']
        print(token)

        details = self.valid_menu
        response = self.client.put("/bookmealapi/v1.0/menu/10",
                                   data=json.dumps(details), content_type='application/json',
                                   headers={'x-access-token': token})
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], "Menu Does Not Exist")

    def test_update_menu_valid(self):
        """ Update Menu """
        user = self.user_admin
        response = self.client.post("/bookmealapi/v1.0/auth/signup",
                                    data=json.dumps(user), content_type='application/json')

        """ correct details admin """
        details = self.login_admin
        response = self.client.post("/bookmealapi/v1.0/auth/login",
                                    data=json.dumps(details), content_type='application/json')
        data = json.loads(response.get_data())
        token = data['token']

        details = self.valid_menu
        response = self.client.post("/bookmealapi/v1.0/menu",
                                    data=json.dumps(details), content_type='application/json',
                                    headers={'x-access-token': token})

        details = {
            "meal_ids": [6, 2, 7, 4],
            "user_id": 1
        }
        response = self.client.put("/bookmealapi/v1.0/menu/1",
                                   data=json.dumps(details), content_type='application/json',
                                   headers={'x-access-token': token})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data())
        self.assertEqual(data['menu']['meal_ids'], [6, 2, 7, 4])

    def test_delete_menu_exists(self):
        """ Deleting a value that exists """
        user = self.user_admin
        response = self.client.post("/bookmealapi/v1.0/auth/signup",
                                    data=json.dumps(user), content_type='application/json')

        """ correct details admin """
        details = self.login_admin
        response = self.client.post("/bookmealapi/v1.0/auth/login",
                                    data=json.dumps(details), content_type='application/json')
        data = json.loads(response.get_data())
        token = data['token']

        details = self.valid_menu
        response = self.client.post("/bookmealapi/v1.0/menu",
                                    data=json.dumps(details), content_type='application/json',
                                    headers={'x-access-token': token})

        response = self.client.delete('/bookmealapi/v1.0/menu/1',
                                      headers={'x-access-token': token})
        self.assertEqual(response.status_code, 200)

    def test_delete_menu_non_existant_data(self):
        """ Deleting menu that doesnt exist """
        user = self.user_admin
        response = self.client.post("/bookmealapi/v1.0/auth/signup",
                                    data=json.dumps(user), content_type='application/json')

        details = self.login_admin
        response = self.client.post("/bookmealapi/v1.0/auth/login",
                                    data=json.dumps(details), content_type='application/json')
        data = json.loads(response.get_data())
        token = data['token']

        response = self.client.delete('/bookmealapi/v1.0/menu/10',
                                      headers={'x-access-token': token})
        self.assertEqual(response.status_code, 404)

    def test_get_menu_day(self):
        """ Get menu  for the day """
        user = self.user_admin
        response = self.client.post("/bookmealapi/v1.0/auth/signup",
                                    data=json.dumps(user), content_type='application/json')

        """ correct details admin """
        details = self.login_admin
        response = self.client.post("/bookmealapi/v1.0/auth/login",
                                    data=json.dumps(details), content_type='application/json')
        data = json.loads(response.get_data())
        token = data['token']

        details = self.valid_menu
        response = self.client.post("/bookmealapi/v1.0/menu",
                                    data=json.dumps(details), content_type='application/json',
                                    headers={'x-access-token': token})

        response = self.client.get('/bookmealapi/v1.0/menu',
                                   headers={'x-access-token': token})
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['menu_day']), 1)
