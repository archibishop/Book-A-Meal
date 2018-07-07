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
        self.vaild_meal = {
            "meal_name": "katogo",
            "price": 2000,
            "meal_type": "breakfast"
        }
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_update_order_missing_values(self):
        """ Missing valuesvin json """
        user = self.user_admin
        response = self.client.post("/bookmealapi/v1.0/auth/signup",
                                    data=json.dumps(user), content_type='application/json')

        details = self.login_admin
        response = self.client.post("/bookmealapi/v1.0/auth/login",
                                    data=json.dumps(details), content_type='application/json')
        data = json.loads(response.get_data())
        token = data['token']

        details = {
            "meal_name":
            "katogo"
        }
        response = self.client.put("/bookmealapi/v1.0/orders/2",
                                   data=json.dumps(details), content_type='application/json',
                                   headers={'x-access-token': token})
        self.assertEqual(response.status_code, 400)

    def test_update_order_price_string(self):
        """  Price cannot be string """
        user = self.user_admin
        response = self.client.post("/bookmealapi/v1.0/auth/signup",
                                    data=json.dumps(user), content_type='application/json')

        details = self.login_admin
        response = self.client.post("/bookmealapi/v1.0/auth/login",
                                    data=json.dumps(details), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        token = data['token']

        details = {
            "meal_name": "katogo",
            "price": "8000"
        }
        response = self.client.put("/bookmealapi/v1.0/orders/2",
                                   data=json.dumps(details), content_type='application/json',
                                   headers={'x-access-token': token})
        self.assertEqual(response.status_code, 400)

    def test_update_order_valid(self):
        """ Update Order """
        user = self.user_admin
        response = self.client.post("/bookmealapi/v1.0/auth/signup",
                                    data=json.dumps(user), content_type='application/json')

        """ correct details admin """
        details = self.login_admin
        response = self.client.post("/bookmealapi/v1.0/auth/login",
                                    data=json.dumps(details), content_type='application/json')
        data = json.loads(response.get_data())
        token = data['token']

        details = self.vaild_meal
        response = self.client.post("/bookmealapi/v1.0/meals",
                                    data=json.dumps(details), content_type='application/json',
                                    headers={'x-access-token': token})

        details = {
            "meal_name": "katogo",
            "price": 2000,
            "user_id": 1
        }
        response = self.client.post("/bookmealapi/v1.0/orders",
                                    data=json.dumps(details), content_type='application/json',
                                    headers={'x-access-token': token})

        details = {
            "meal_name": "katogo",
            "price": 8000
        }
        response = self.client.put("/bookmealapi/v1.0/orders/1",
                                   data=json.dumps(details), content_type='application/json',
                                   headers={'x-access-token': token})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data())
        # self.assertEqual(data['order']['id'], 2)
        self.assertEqual(data['order']['meal_name'], "katogo")
        self.assertEqual(data['order']['price'], 8000)

    def test_delete_order_non_existant_data(self):
        """ Deleting order that doesnt exist """
        user = self.user_admin
        response = self.client.post("/bookmealapi/v1.0/auth/signup",
                                    data=json.dumps(user), content_type='application/json')

        details = self.login_admin
        response = self.client.post("/bookmealapi/v1.0/auth/login",
                                    data=json.dumps(details), content_type='application/json')
        data = json.loads(response.get_data())
        token = data['token']

        response = self.client.delete('/bookmealapi/v1.0/orders/10',
                                      headers={'x-access-token': token})
        self.assertEqual(response.status_code, 404)

    def test_delete_order_data_exists(self):
        """ Deleting an order """
        user = self.user_admin
        response = self.client.post("/bookmealapi/v1.0/auth/signup",
                                    data=json.dumps(user), content_type='application/json')

        """ correct details admin """
        details = self.login_admin
        response = self.client.post("/bookmealapi/v1.0/auth/login",
                                    data=json.dumps(details), content_type='application/json')
        data = json.loads(response.get_data())
        token = data['token']

        details = self.vaild_meal
        response = self.client.post("/bookmealapi/v1.0/meals",
                                    data=json.dumps(details), content_type='application/json',
                                    headers={'x-access-token': token})

        details = {
            "meal_name": "katogo",
            "price": 2000,
            "user_id": 1
        }
        response = self.client.post("/bookmealapi/v1.0/orders",
                                    data=json.dumps(details), content_type='application/json',
                                    headers={'x-access-token': token})

        response = self.client.delete('/bookmealapi/v1.0/orders/1',
                                      headers={'x-access-token': token})
        self.assertEqual(response.status_code, 200)

    def test_get_all_orders(self):
        """ Get All orders """
        user = self.user_admin
        response = self.client.post("/bookmealapi/v1.0/auth/signup",
                                    data=json.dumps(user), content_type='application/json')

        """ correct details admin """
        details = self.login_admin
        response = self.client.post("/bookmealapi/v1.0/auth/login",
                                    data=json.dumps(details), content_type='application/json')
        data = json.loads(response.get_data())
        token = data['token']

        details = self.vaild_meal
        response = self.client.post("/bookmealapi/v1.0/meals",
                                    data=json.dumps(details), content_type='application/json',
                                    headers={'x-access-token': token})

        details = {
            "meal_name": "katogo",
            "price": 2000,
            "user_id": 1
        }
        response = self.client.post("/bookmealapi/v1.0/orders",
                                    data=json.dumps(details), content_type='application/json',
                                    headers={'x-access-token': token})

        response = self.client.get('/bookmealapi/v1.0/orders',
                                   headers={'x-access-token': token})
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['transactions']), 1)
