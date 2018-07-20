from api import create_app
from api import db
from flask import current_app
from api.models.models import User, Menu, Order, Meal
# from api.models.models import User
# # from api.models.models import Menu
# # from api.models.models import Orders
# from api.models.Meals import Meals
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

    def test_add_meal(self):
        """ missing values """
        user = self.user_admin
        response = self.client.post("/bookmealapi/v1.0/auth/signup",
                                    data=json.dumps(user), content_type='application/json')


        details = self.login_admin
        response = self.client.post("/bookmealapi/v1.0/auth/login",
                                    data=json.dumps(details), content_type='application/json')
        data = json.loads(response.get_data())
        token = data['token']

        details = {
            "meal_name": "katogo"
        }
        response = self.client.post(
            "/bookmealapi/v1.0/meals", data=json.dumps(details),
            content_type='application/json',
            headers={'x-access-token': token})
        print(token)
        self.assertEqual(response.status_code, 400)

    def test_add_meal_price_is_string(self):
        """ # price cannot take string """
        user = self.user_admin
        response = self.client.post("/bookmealapi/v1.0/auth/signup",
                                    data=json.dumps(user), content_type='application/json')


        details = self.login_admin
        response = self.client.post("/bookmealapi/v1.0/auth/login",
                                    data=json.dumps(details), content_type='application/json')
        data = json.loads(response.get_data())
        token = data['token']

        details = {
            "mealname": "katogo",
            "price": "2000",
            "meal_type": "breakfast"
        }
        response = self.client.post("/bookmealapi/v1.0/meals",
                                    data=json.dumps(details), content_type='application/json',
                                    headers={'x-access-token': token})
        self.assertEqual(response.status_code, 400)

    def test_add_meal_valid(self):
        """ correct values """
        user = self.user_admin
        response = self.client.post("/bookmealapi/v1.0/auth/signup",
                                    data=json.dumps(user), content_type='application/json')


        details = self.login_admin
        response = self.client.post("/bookmealapi/v1.0/auth/login",
                                    data=json.dumps(details), content_type='application/json')
        data = json.loads(response.get_data())
        token = data['token']

        details = self.vaild_meal
        response = self.client.post("/bookmealapi/v1.0/meals",
                                    data=json.dumps(details), content_type='application/json',
                                    headers={'x-access-token': token})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], "Meal Successfully Added")

        #same meal name
        details = self.vaild_meal
        response = self.client.post("/bookmealapi/v1.0/meals",
                                    data=json.dumps(details), content_type='application/json',
                                    headers={'x-access-token': token})
        self.assertEqual(response.status_code, 400)

    def test_select_meal_missing_values(self):
        """  Mising Values in json """
        user = self.user_admin
        response = self.client.post("/bookmealapi/v1.0/auth/signup",
                                    data=json.dumps(user), content_type='application/json')

        """ correct details """
        details = self.login_admin
        response = self.client.post("/bookmealapi/v1.0/auth/login",
                                    data=json.dumps(details), content_type='application/json')
        data = json.loads(response.get_data())
        token = data['token']

        details = {
            "meal_name": "katogo"
        }
        response = self.client.post("/bookmealapi/v1.0/orders",
                                    data=json.dumps(details), content_type='application/json',
                                    headers={'x-access-token': token})
        self.assertEqual(response.status_code, 400)

    def test_select_meal_price_user_id_string(self):
        """  Price and userId cannot be string """
        user = {
            "fname": "toast",
            "lname": "bull",
            "email": "tbull@gmail.com",
            "password": "12345",
            "role_id": 2
        }
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
        token = data['token']

        details = {
            "meal_name": "katogo",
            "price": "2000",
            "user_id": "2"
        }
        response = self.client.post("/bookmealapi/v1.0/orders",
                                    data=json.dumps(details), content_type='application/json',
                                    headers={'x-access-token': token})
        self.assertEqual(response.status_code, 400)

    def test_select_meal_valid(self):
        """  valid json """
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
            "user_id": 1
        }
        response = self.client.post("/bookmealapi/v1.0/orders",
                                    data=json.dumps(details), content_type='application/json',
                                    headers={'x-access-token': token})
        self.assertEqual(response.status_code, 201)

    def test_delete_meal_option_non_existant_data(self):
        """ Deleting a value that doesnt exist """
        user = self.user_admin
        response = self.client.post("/bookmealapi/v1.0/auth/signup",
                                    data=json.dumps(user), content_type='application/json')

        details = {
            "email": "steven@gmail.com",
            "password": "54321"
        }
        response = self.client.post("/bookmealapi/v1.0/auth/login",
                                    data=json.dumps(details), content_type='application/json')
        data = json.loads(response.get_data())
        token = data['token']

        response = self.client.delete('/bookmealapi/v1.0/meals/10',
                                      headers={'x-access-token': token})
        self.assertEqual(response.status_code, 404)

    def test_delete_meal_option_data_exists(self):
        """ Deleting a value that exists """
        user = self.user_admin
        response = self.client.post("/bookmealapi/v1.0/auth/signup",
                                    data=json.dumps(user), content_type='application/json')

        details = self.login_admin
        response = self.client.post("/bookmealapi/v1.0/auth/login",
                                    data=json.dumps(details), content_type='application/json')
        data = json.loads(response.get_data())
        token = data['token']

        details = self.vaild_meal
        response = self.client.post("/bookmealapi/v1.0/meals",
                                    data=json.dumps(details), content_type='application/json',
                                    headers={'x-access-token': token})

        response = self.client.delete('/bookmealapi/v1.0/meals/1',
                                      headers={'x-access-token': token})
        self.assertEqual(response.status_code, 200)

    def test_update_meal_option(self):
        """ # missing values """

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
            "meal_name": "katogo"
        }
        response = self.client.put("/bookmealapi/v1.0/meals/2",
                                   data=json.dumps(details), content_type='application/json',
                                   headers={'x-access-token': token})
        self.assertEqual(response.status_code, 400)

    def test_update_meal_option_price_string(self):
        """ Price cannot be string """
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
        response = self.client.put("/bookmealapi/v1.0/meals/2",
                                   data=json.dumps(details), content_type='application/json',
                                   headers={'x-access-token': token})
        self.assertEqual(response.status_code, 400)

    def test_update_meal_option_valid(self):
        """ correct values """
        user = self.user_admin
        response = self.client.post("/bookmealapi/v1.0/auth/signup",
                                    data=json.dumps(user), content_type='application/json')

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
            "meal_name": "rolex",
            "price": 8000,
            "meal_type": "breakfast"
        }
        response = self.client.put("/bookmealapi/v1.0/meals/1",
                                   data=json.dumps(details), content_type='application/json',
                                   headers={'x-access-token': token})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data())
        self.assertEqual(data['meal']['meal_name'], "rolex")
        self.assertEqual(data['meal']['price'], 8000)
        self.assertEqual(data['meal']['meal_type'], "breakfast")

    def test_get_all_meals(self):
        """ Get all meals """
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

        response = self.client.get('/bookmealapi/v1.0/meals',
                                   headers={'x-access-token': token})
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['meals']), 1)
