""" import context """
from app import app
from api import db
from api import User, Admin, Meals, Orders, Menu
from werkzeug.security import generate_password_hash, check_password_hash
import unittest
import json


BASE_URL = 'http://127.0.0.1:5000/bookmealapi/v1.0/meals/'


class api_test_case(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] =\
         "postgresql://postgres:12345@localhost/test_book"
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.drop_all()    

    def test_signup_missing_values(self):
        """ missing value in request sent"""
        user = {
            "fname": "brian", 
            "lname": "Wagubi", 
            "password": "12345"
        }
        response = self.app.post("/bookmealapi/v1.0/auth/signup",\
            data=json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_signup_valid(self):
        """ valid json object, all fields avaiable """
        user = {
            "fname": "clap",
            "lname": "flip", 
            "email": "clap@gmail.com",
            "password": "12345",
            "role_id": 2
        }
        response = self.app.post("/bookmealapi/v1.0/auth/signup",\
            data=json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'New user created!')

        """ cannot add item with same email again """
        user = {
            "fname": "clap", 
            "lname": "flip",
            "email": "clap@gmail.com",
            "password": "12345",
            "role_id": 2
        }
        response = self.app.post("/bookmealapi/v1.0/auth/signup",\
            data=json.dumps(user), content_type='application/json')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], "Email Already Exists")

    def test_login_missing_values(self):
        """ missing values in json  """
        details = {
            "email": "wagubib@gmail.com"
        }
        response = self.app.post("/bookmealapi/v1.0/auth/login",\
            data=json.dumps(details), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_login_valid_details_user(self):
        """
        user = {
            "fname": "toast", 
            "lname": "bull",
            "email": "tbull@gmail.com",
            "password": "12345"
        }
        response = self.app.post("/bookmealapi/v1.0/auth/signup",\
            data=json.dumps(user), content_type='application/json')
        """
        first_name = "toast"
        last_name = "bull"
        email = "tbull@gmail.com"
        password = "12345"
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(first_name=first_name, last_name=last_name,\
          email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()      

        """ correct details """
        details = {
            "email": "tbull@gmail.com",
            "password": "12345"
        }

        response = self.app.post("/bookmealapi/v1.0/auth/login",\
            data=json.dumps(details), content_type='application/json')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], "Successfully login")

    def test_login_valid_details_user2(self):
        first_name = "atlas"
        last_name = "waters"
        email = "atlas@gmail.com"
        password = "12345"
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(first_name=first_name, last_name=last_name,\
          email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit() 

        """ correct details """
        details = {
            "email": "atlas@gmail.com",
            "password": "12345"
        }
        response = self.app.post("/bookmealapi/v1.0/auth/login",\
            data=json.dumps(details), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], "Successfully login")

    def test_login_valid_details_admin(self):
        business_name = "FAST FOOD"
        location = "nakulabye"
        first_name = "atlas"
        last_name = "waters"
        email = "steven@gmail.com"
        password = "54321"
        role_id = 1
        hashed_password = generate_password_hash(password, method='sha256')
        new_admin = User(first_name= first_name, last_name=last_name,\
                      email=email, password= hashed_password, role_id=role_id,\
                      business_name=business_name, location=location)

        db.session.add(new_admin)
        db.session.commit()

        """ correct details admin """
        details = {
            "email": "steven@gmail.com",
            "password": "54321"
        }
        response = self.app.post("/bookmealapi/v1.0/auth/login",\
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
        response = self.app.post("/bookmealapi/v1.0/auth/login",\
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
        response = self.app.post("/bookmealapi/v1.0/auth/login",\
            data=json.dumps(details), content_type='application/json')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], "User Not Found")

    def test_add_meal(self):
        """ missing values """
        business_name = "FAST FOOD"
        location = "nakulabye"
        first_name = "atlas"
        last_name = "waters"
        email = "steven@gmail.com"
        password = "54321"
        role_id = 1
        hashed_password = generate_password_hash(password, method='sha256')
        new_admin = User(first_name= first_name, last_name=last_name,\
                      email=email, password= hashed_password, role_id=role_id,\
                      business_name=business_name, location=location)
        db.session.add(new_admin)
        db.session.commit()

        """ correct details admin """
        details = {
            "email": "steven@gmail.com",
            "password": "54321"
        }
        response = self.app.post("/bookmealapi/v1.0/auth/login",\
            data=json.dumps(details), content_type='application/json')
        data = json.loads(response.get_data())
        token = data['token']

        details = {
            "mealname": "katogo"
        }
        response = self.app.post(
            "/bookmealapi/v1.0/meals", data=json.dumps(details),\
             content_type='application/json',\
            headers={'x-access-token' : token})
        self.assertEqual(response.status_code, 400)

    def test_add_meal_price_is_string(self):
        """ # price cannot take string """
        business_name = "FAST FOOD"
        location = "nakulabye"
        first_name = "atlas"
        last_name = "waters"
        email = "steven@gmail.com"
        password = "54321"
        role_id = 1
        hashed_password = generate_password_hash(password, method='sha256')
        new_admin = User(first_name= first_name, last_name=last_name,\
                      email=email, password= hashed_password, role_id=role_id,\
                      business_name=business_name, location=location)
        db.session.add(new_admin)
        db.session.commit()

        """ correct details admin """
        details = {
            "email": "steven@gmail.com",
            "password": "54321"
        }
        response = self.app.post("/bookmealapi/v1.0/auth/login",\
            data=json.dumps(details), content_type='application/json')
        data = json.loads(response.get_data())
        token = data['token']

        details = {
            "mealname": "katogo", 
            "price": "2000", 
            "meal_type": "breakfast"
        }
        response = self.app.post("/bookmealapi/v1.0/meals",\
            data=json.dumps(details), content_type='application/json',\
            headers={'x-access-token' : token})
        self.assertEqual(response.status_code, 400)

    def test_add_meal_valid(self):
        """ correct values """
        business_name = "FAST FOOD"
        location = "nakulabye"
        first_name = "atlas"
        last_name = "waters"
        email = "steven@gmail.com"
        password = "54321"
        role_id = 1
        hashed_password = generate_password_hash(password, method='sha256')
        new_admin = User(first_name= first_name, last_name=last_name,\
                      email=email, password= hashed_password, role_id=role_id,\
                      business_name=business_name, location=location)
        db.session.add(new_admin)
        db.session.commit()

        """ correct details admin """
        details = {
            "email": "steven@gmail.com",
            "password": "54321"
        }
        response = self.app.post("/bookmealapi/v1.0/auth/login",\
            data=json.dumps(details), content_type='application/json')
        data = json.loads(response.get_data())
        token = data['token']

        details = {
            "meal_name": "katogo", 
            "price": 2000, 
            "meal_type": "breakfast"
        }
        response = self.app.post("/bookmealapi/v1.0/meals",\
            data=json.dumps(details), content_type='application/json',\
            headers={'x-access-token' : token})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], "Meal Successfully Added")

        #same meal name
        details = {
            "meal_name": "katogo", 
            "price": 2000, 
            "meal_type": "breakfast"
        }
        response = self.app.post("/bookmealapi/v1.0/meals",\
            data=json.dumps(details), content_type='application/json',\
            headers={'x-access-token' : token})
        self.assertEqual(response.status_code, 400)

    def test_select_meal_missing_values(self):
        """  Mising Values in json """
        first_name = "atlas"
        last_name = "waters"
        email = "atlas@gmail.com"
        password = "12345"
        role_id = 2
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(first_name= first_name, last_name=last_name,\
                      email=email, password= hashed_password, role_id=role_id)
        db.session.add(new_user)
        db.session.commit() 

        """ correct details """
        details = {
            "email": "atlas@gmail.com",
            "password": "12345"
        }
        response = self.app.post("/bookmealapi/v1.0/auth/login",\
            data=json.dumps(details), content_type='application/json')
        data = json.loads(response.get_data())
        token = data['token']

        details = {
            "meal_name": "katogo"
        }
        response = self.app.post("/bookmealapi/v1.0/orders",
                data=json.dumps(details), content_type='application/json',\
                headers={'x-access-token' : token})
        self.assertEqual(response.status_code, 400)

    def test_select_meal_price_user_id_string(self):
        """  Price and userId cannot be string """
        first_name = "atlas"
        last_name = "waters"
        email = "atlas@gmail.com"
        password = "12345"
        role_id = 2
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(first_name= first_name, last_name=last_name,\
                      email=email, password= hashed_password, role_id=role_id)
        db.session.add(new_user)
        db.session.commit() 

        """ correct details """
        details = {
            "email": "atlas@gmail.com",
            "password": "12345"
        }
        response = self.app.post("/bookmealapi/v1.0/auth/login",\
            data=json.dumps(details), content_type='application/json')
        data = json.loads(response.get_data())
        token = data['token']

        details = {
            "meal_name": "katogo",
            "price": "2000", 
            "userId": "2"
        }
        response = self.app.post("/bookmealapi/v1.0/orders",\
            data=json.dumps(details), content_type='application/json',\
                headers={'x-access-token' : token})
        self.assertEqual(response.status_code, 400)

    def test_select_meal_valid(self):
        """  valid json """
        first_name = "atlas"
        last_name = "waters"
        email = "atlas@gmail.com"
        password = "12345"
        role_id = 2
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(first_name= first_name, last_name=last_name,\
                      email=email, password= hashed_password, role_id=role_id)
        db.session.add(new_user)
        db.session.commit() 

        meal_name = "katogo"
        price = 2000
        meal_type = "breakfast"
        meal = Meals(meal_name=meal_name, price=price, meal_type=meal_type)
        db.session.add(meal)
        db.session.commit()

        """ correct details """
        details = {
            "email": "atlas@gmail.com",
            "password": "12345"
        }
        response = self.app.post("/bookmealapi/v1.0/auth/login",\
            data=json.dumps(details), content_type='application/json')
        data = json.loads(response.get_data())
        token = data['token']

        details = {
            "meal_name": "katogo", 
            "price": 2000, 
            "userId": 1
        }
        response = self.app.post("/bookmealapi/v1.0/orders",\
            data=json.dumps(details), content_type='application/json',\
                headers={'x-access-token' : token})
        self.assertEqual(response.status_code, 201)

    def test_set_menu(self):
        """ setting the menu """
        business_name = "FAST FOOD"
        location = "nakulabye"
        first_name = "atlas"
        last_name = "waters"
        email = "steven@gmail.com"
        password = "54321"
        role_id = 1
        hashed_password = generate_password_hash(password, method='sha256')
        new_admin = User(first_name= first_name, last_name=last_name,\
                      email=email, password= hashed_password, role_id=role_id,\
                      business_name=business_name, location=location)
        db.session.add(new_admin)
        db.session.commit()


        """ correct details admin """
        details = {
            "email": "steven@gmail.com",
            "password": "54321"
        }
        response = self.app.post("/bookmealapi/v1.0/auth/login",\
            data=json.dumps(details), content_type='application/json')
        data = json.loads(response.get_data())
        token = data['token']

        """
        details = {
            "meal_name": "rolex", 
            "price": 2000, 
            "meal_type": "breakfast"
        }
        """

        details = {
            "meal_ids": [1, 2, 3, 4],
            "user_id": 1
        }
        response = self.app.post("/bookmealapi/v1.0/menu",
                data=json.dumps(details), content_type='application/json',\
                headers={'x-access-token' : token})
        self.assertEqual(response.status_code, 201)

    def test_delete_meal_option_non_existant_data(self):
        """ Deleting a value that doesnt exist """
        business_name = "FAST FOOD"
        location = "nakulabye"
        first_name = "atlas"
        last_name = "waters"
        email = "steven@gmail.com"
        password = "54321"
        role_id = 1
        hashed_password = generate_password_hash(password, method='sha256')
        new_admin = User(first_name= first_name, last_name=last_name,\
                      email=email, password= hashed_password, role_id=role_id,\
                      business_name=business_name, location=location)
        db.session.add(new_admin)
        db.session.commit()

        details = {
            "email": "steven@gmail.com", 
            "password": "54321"
        }
        response = self.app.post("/bookmealapi/v1.0/auth/login",\
            data=json.dumps(details), content_type='application/json')
        data = json.loads(response.get_data())
        token = data['token']

        response = self.app.delete('/bookmealapi/v1.0/meals/10',\
                headers={'x-access-token' : token})
        self.assertEqual(response.status_code, 404)

    def test_delete_meal_option_data_exists(self):
        """ Deleting a value that exists """
        business_name = "FAST FOOD"
        location = "nakulabye"
        first_name = "atlas"
        last_name = "waters"
        email = "steven@gmail.com"
        password = "54321"
        role_id = 1
        hashed_password = generate_password_hash(password, method='sha256')
        new_admin = User(first_name= first_name, last_name=last_name,\
                      email=email, password= hashed_password, role_id=role_id,\
                      business_name=business_name, location=location)
        db.session.add(new_admin)
        db.session.commit()

        meal_name = "katogo"
        price = 2000
        meal_type = "breakfast"
        meal = Meals(meal_name=meal_name, price=price, meal_type=meal_type)
        db.session.add(meal)
        db.session.commit()
        
        details = {
            "email": "steven@gmail.com", 
            "password": "54321"
        }
        response = self.app.post("/bookmealapi/v1.0/auth/login",\
            data=json.dumps(details), content_type='application/json')
        data = json.loads(response.get_data())
        token = data['token']

        response = self.app.delete('/bookmealapi/v1.0/meals/1',\
                headers={'x-access-token' : token})
        self.assertEqual(response.status_code, 200)
    

    def test_update_meal_option(self):
        """ # missing values """

        business_name = "FAST FOOD"
        location = "nakulabye"
        first_name = "atlas"
        last_name = "waters"
        email = "steven@gmail.com"
        password = "54321"
        role_id = 1
        hashed_password = generate_password_hash(password, method='sha256')
        new_admin = User(first_name= first_name, last_name=last_name,\
                      email=email, password= hashed_password, role_id=role_id,\
                      business_name=business_name, location=location)
        db.session.add(new_admin)
        db.session.commit()

        details = {
            "email": "steven@gmail.com", 
            "password": "54321"
        }
        response = self.app.post("/bookmealapi/v1.0/auth/login",\
            data=json.dumps(details), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        token = data['token']

        details = {
            "meal_name": "katogo"
        }
        response = self.app.put("/bookmealapi/v1.0/meals/2",\
            data=json.dumps(details), content_type='application/json',\
                headers={'x-access-token' : token})
        self.assertEqual(response.status_code, 400)

    def test_update_meal_option_price_string(self):
        """ Price cannot be string """
        business_name = "FAST FOOD"
        location = "nakulabye"
        first_name = "atlas"
        last_name = "waters"
        email = "steven@gmail.com"
        password = "54321"
        role_id = 1
        hashed_password = generate_password_hash(password, method='sha256')
        new_admin = User(first_name= first_name, last_name=last_name,\
                      email=email, password= hashed_password, role_id=role_id,\
                      business_name=business_name, location=location)
        db.session.add(new_admin)
        db.session.commit()
        
        details = {
            "email": "steven@gmail.com", 
            "password": "54321"
        }
        response = self.app.post("/bookmealapi/v1.0/auth/login",\
            data=json.dumps(details), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        token = data['token']

        details = {
            "meal_name": "katogo", 
            "price": "8000"
        }
        response = self.app.put("/bookmealapi/v1.0/meals/2",\
            data=json.dumps(details), content_type='application/json',\
                headers={'x-access-token' : token})
        self.assertEqual(response.status_code, 400)

    def test_update_meal_option_valid(self):
        """ correct values """
        business_name = "FAST FOOD"
        location = "nakulabye"
        first_name = "atlas"
        last_name = "waters"
        email = "steven@gmail.com"
        password = "54321"
        role_id = 1
        hashed_password = generate_password_hash(password, method='sha256')
        new_admin = User(first_name= first_name, last_name=last_name,\
                      email=email, password= hashed_password, role_id=role_id,\
                      business_name=business_name, location=location)
        db.session.add(new_admin)
        db.session.commit()

        meal_name = "katogo"
        price = 2000
        meal_type = "lunch"
        meal = Meals(meal_name=meal_name, price=price, meal_type=meal_type)
        db.session.add(meal)
        db.session.commit()
        
        details = {
            "email": "steven@gmail.com", 
            "password": "54321"
        }

        response = self.app.post("/bookmealapi/v1.0/auth/login",\
            data=json.dumps(details), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        token = data['token']

        details = {
            "meal_name": "rolex", 
            "price": 8000, 
            "meal_type": "breakfast"
        }
        response = self.app.put("/bookmealapi/v1.0/meals/1",\
            data=json.dumps(details), content_type='application/json',\
            headers={'x-access-token' : token})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data())
        # self.assertEqual(data['meal']['id'], 2)
        self.assertEqual(data['meal']['meal_name'], "rolex")
        self.assertEqual(data['meal']['price'], 8000)
        self.assertEqual(data['meal']['meal_type'], "breakfast")

    def test_update_order_missing_values(self):
        """ Missing valuesvin json """
        business_name = "FAST FOOD"
        location = "nakulabye"
        first_name = "atlas"
        last_name = "waters"
        email = "steven@gmail.com"
        password = "54321"
        role_id = 1
        hashed_password = generate_password_hash(password, method='sha256')
        new_admin = User(first_name= first_name, last_name=last_name,\
                      email=email, password= hashed_password, role_id=role_id,\
                      business_name=business_name, location=location)
        db.session.add(new_admin)
        db.session.commit()

        details = {
            "email": "steven@gmail.com", 
            "password": "54321"
        }
        response = self.app.post("/bookmealapi/v1.0/auth/login",\
            data=json.dumps(details), content_type='application/json')
        data = json.loads(response.get_data())
        token = data['token']

        details = {
            "meal_name": 
            "katogo"
        }
        response = self.app.put("/bookmealapi/v1.0/orders/2",\
                data=json.dumps(details), content_type='application/json',\
                headers={'x-access-token' : token})
        self.assertEqual(response.status_code, 400)

    def test_update_order_price_string(self):
        """  Price cannot be string """
        business_name = "FAST FOOD"
        location = "nakulabye"
        first_name = "atlas"
        last_name = "waters"
        email = "steven@gmail.com"
        password = "54321"
        role_id = 1
        hashed_password = generate_password_hash(password, method='sha256')
        new_admin = User(first_name= first_name, last_name=last_name,\
                      email=email, password= hashed_password, role_id=role_id,\
                      business_name=business_name, location=location)
        db.session.add(new_admin)
        db.session.commit()

        details = {
            "email": "steven@gmail.com", 
            "password": "54321"
        }
        response = self.app.post("/bookmealapi/v1.0/auth/login",\
            data=json.dumps(details), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        token = data['token']

        details = {
            "meal_name": "katogo", 
            "price": "8000"
        }
        response = self.app.put("/bookmealapi/v1.0/orders/2",\
                data=json.dumps(details), content_type='application/json',\
                headers={'x-access-token' : token})
        self.assertEqual(response.status_code, 400)

    def test_update_order_valid(self):
        """ Update Order """
        first_name = "atlas"
        last_name = "waters"
        email = "atlas@gmail.com"
        password = "12345"
        role_id = 2
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(first_name= first_name, last_name=last_name,\
                      email=email, password= hashed_password, role_id=role_id)
        db.session.add(new_user)
        db.session.commit() 

        meal_name = "katogo"
        price = 3000
        process_status = "Pending"
        user_id = 1
        order = Orders(meal_name=meal_name, price=price, user_id=user_id,\
         process_status=process_status)
        db.session.add(order)
        db.session.commit()

        details = {
            "email": "atlas@gmail.com", 
            "password": "12345"
        }
        response = self.app.post("/bookmealapi/v1.0/auth/login",\
            data=json.dumps(details), content_type='application/json')
        data = json.loads(response.get_data())
        token = data['token']

        details = {
            "meal_name": "katogo",
            "price": 8000
        }
        response = self.app.put("/bookmealapi/v1.0/orders/1",
                data=json.dumps(details), content_type='application/json',\
                headers={'x-access-token' : token})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data())
        # self.assertEqual(data['order']['id'], 2)
        self.assertEqual(data['order']['meal_name'], "katogo")
        self.assertEqual(data['order']['price'], 8000)

    def test_update_menu_missing_value(self):
        """ Incomplete json sent """
        business_name = "FAST FOOD"
        location = "nakulabye"
        first_name = "atlas"
        last_name = "waters"
        email = "steven@gmail.com"
        password = "54321"
        role_id = 1
        hashed_password = generate_password_hash(password, method='sha256')
        new_admin = User(first_name= first_name, last_name=last_name,\
                      email=email, password= hashed_password, role_id=role_id,\
                      business_name=business_name, location=location)
        db.session.add(new_admin)
        db.session.commit()

        details = {
            "email": "steven@gmail.com", 
            "password": "54321"
        }
        response = self.app.post("/bookmealapi/v1.0/auth/login",\
            data=json.dumps(details), content_type='application/json')
        data = json.loads(response.get_data())
        token = data['token']

        details = {
            "user_id": 3
        }
        response = self.app.put("/bookmealapi/v1.0/menu/1",
                data=json.dumps(details), content_type='application/json',\
                headers={'x-access-token' : token})
        self.assertEqual(response.status_code, 400) 

    def test_update_menu_nonexistant(self):
        """ Incomplete json sent """
        business_name = "FAST FOOD"
        location = "nakulabye"
        first_name = "atlas"
        last_name = "waters"
        email = "steven@gmail.com"
        password = "54321"
        role_id = 1
        hashed_password = generate_password_hash(password, method='sha256')
        new_admin = User(first_name= first_name, last_name=last_name,\
                      email=email, password= hashed_password, role_id=role_id,\
                      business_name=business_name, location=location)
        db.session.add(new_admin)
        db.session.commit()

        details = {
            "email": "steven@gmail.com", 
            "password": "54321"
        }
        response = self.app.post("/bookmealapi/v1.0/auth/login",\
            data=json.dumps(details), content_type='application/json')
        data = json.loads(response.get_data())
        token = data['token']

        details = {
            "meal_ids": [6, 2, 7, 4],
            "user_id": 3
        }
        response = self.app.put("/bookmealapi/v1.0/menu/10",
                data=json.dumps(details), content_type='application/json',\
                headers={'x-access-token' : token})
        self.assertEqual(response.status_code, 404) 
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], "Menu Does Not Exist")     

    def test_update_menu_valid(self):
        """ Update Menu """
        business_name = "FAST FOOD"
        location = "nakulabye"
        first_name = "atlas"
        last_name = "waters"
        email = "steven@gmail.com"
        password = "54321"
        role_id = 1
        hashed_password = generate_password_hash(password, method='sha256')
        new_admin = User(first_name= first_name, last_name=last_name,\
                      email=email, password= hashed_password, role_id=role_id,\
                      business_name=business_name, location=location)
        db.session.add(new_admin)
        db.session.commit()

        meal_ids =[6, 2, 7, 4]
        meal_ids_string = ""
        for ids in meal_ids:
            meal_ids_string += ';%s' % ids 
        user_id = 1
        menu = Menu(user_id=user_id, meal_ids=meal_ids_string)
        db.session.add(menu)
        db.session.commit()

        details = {
            "email": "steven@gmail.com", 
            "password": "54321"
        }
        response = self.app.post("/bookmealapi/v1.0/auth/login",\
            data=json.dumps(details), content_type='application/json')
        data = json.loads(response.get_data())
        token = data['token']

        details = {
            "meal_ids": [6, 2, 7, 4],
            "user_id": 3
        }
        response = self.app.put("/bookmealapi/v1.0/menu/1",
                data=json.dumps(details), content_type='application/json',\
                headers={'x-access-token' : token})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data())
        self.assertEqual(data['menu']['meal_ids'], [6, 2, 7, 4])
        

    def test_get_all_meals(self):
        """ Get all meals """
        business_name = "FAST FOOD"
        location = "nakulabye"
        first_name = "atlas"
        last_name = "waters"
        email = "steven@gmail.com"
        password = "54321"
        role_id = 1
        hashed_password = generate_password_hash(password, method='sha256')
        new_admin = User(first_name= first_name, last_name=last_name,\
                      email=email, password= hashed_password, role_id=role_id,\
                      business_name=business_name, location=location)
        db.session.add(new_admin)
        db.session.commit()

        meal_name = "katogo"
        price = 2000
        meal_type = "breakfast"
        meal = Meals(meal_name=meal_name, price=price, meal_type=meal_type)
        db.session.add(meal)
        db.session.commit()

        details = {
            "email": "steven@gmail.com", 
            "password": "54321"
        }
        response = self.app.post("/bookmealapi/v1.0/auth/login",\
            data=json.dumps(details), content_type='application/json')
        data = json.loads(response.get_data())
        token = data['token']

        response = self.app.get('/bookmealapi/v1.0/meals',\
                headers={'x-access-token' : token})
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['meals']), 1)

    def test_get_all_orders(self):
        """ Get All orders """
        business_name = "FAST FOOD"
        location = "nakulabye"
        first_name = "atlas"
        last_name = "waters"
        email = "steven@gmail.com"
        password = "54321"
        role_id = 1
        hashed_password = generate_password_hash(password, method='sha256')
        new_admin = User(first_name= first_name, last_name=last_name,\
                      email=email, password= hashed_password, role_id=role_id,\
                      business_name=business_name, location=location)
        db.session.add(new_admin)
        db.session.commit()

        """ To pass the test """
        first_name = "atlas"
        last_name = "waters"
        email = "atlas@gmail.com"
        password = "12345"
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(first_name=first_name, last_name=last_name,\
          email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit() 

        meal_name = "katogo"
        price = 3000
        process_status = "Pending"
        user_id = 1
        order = Orders(meal_name=meal_name, price=price, user_id=user_id,\
         process_status=process_status)
        db.session.add(order)
        db.session.commit()

        details = {
            "email": "steven@gmail.com", 
            "password": "54321"
        }
        response = self.app.post("/bookmealapi/v1.0/auth/login",\
            data=json.dumps(details), content_type='application/json')
        data = json.loads(response.get_data())
        token = data['token']

        response = self.app.get('/bookmealapi/v1.0/orders',\
                headers={'x-access-token' : token})
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['transactions']), 1)

    def test_get_menu_day(self):
        """ Get menu  for the day """
        business_name = "FAST FOOD"
        location = "nakulabye"
        first_name = "atlas"
        last_name = "waters"
        email = "steven@gmail.com"
        password = "54321"
        role_id = 1
        hashed_password = generate_password_hash(password, method='sha256')
        new_admin = User(first_name= first_name, last_name=last_name,\
                      email=email, password= hashed_password, role_id=role_id,\
                      business_name=business_name, location=location)
        db.session.add(new_admin)
        db.session.commit()

        """ To pass the test """
        first_name = "atlas"
        last_name = "waters"
        email = "atlas@gmail.com"
        password = "12345"
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(first_name=first_name, last_name=last_name,\
          email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit() 

        meal_ids =[6, 2, 7, 4]
        meal_ids_string = ""
        for ids in meal_ids:
            meal_ids_string += ';%s' % ids 
        user_id = 1
        menu = Menu(user_id=user_id, meal_ids=meal_ids_string)
        db.session.add(menu)
        db.session.commit()

        details = {
            "email": "atlas@gmail.com", 
            "password": "12345"
        }
        response = self.app.post("/bookmealapi/v1.0/auth/login",\
            data=json.dumps(details), content_type='application/json')
        data = json.loads(response.get_data())
        token = data['token']

        response = self.app.get('/bookmealapi/v1.0/menu',\
                headers={'x-access-token' : token})
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['menu_day']), 1)

    def test_delete_order_non_existant_data(self):
        """ Deleting order that doesnt exist """
        business_name = "FAST FOOD"
        location = "nakulabye"
        first_name = "atlas"
        last_name = "waters"
        email = "steven@gmail.com"
        password = "54321"
        role_id = 1
        hashed_password = generate_password_hash(password, method='sha256')
        new_admin = User(first_name= first_name, last_name=last_name,\
                      email=email, password= hashed_password, role_id=role_id,\
                      business_name=business_name, location=location)
        db.session.add(new_admin)
        db.session.commit()

        details = {
            "email": "steven@gmail.com", 
            "password": "54321"
        }
        response = self.app.post("/bookmealapi/v1.0/auth/login",\
            data=json.dumps(details), content_type='application/json')
        data = json.loads(response.get_data())
        token = data['token']

        response = self.app.delete('/bookmealapi/v1.0/orders/10',\
                headers={'x-access-token' : token})
        self.assertEqual(response.status_code, 404)

    
    def test_delete_order_data_exists(self):
        """ Deleting an order """
        business_name = "FAST FOOD"
        location = "nakulabye"
        first_name = "atlas"
        last_name = "waters"
        email = "steven@gmail.com"
        password = "54321"
        role_id = 1
        hashed_password = generate_password_hash(password, method='sha256')
        new_admin = User(first_name= first_name, last_name=last_name,\
                      email=email, password= hashed_password, role_id=role_id,\
                      business_name=business_name, location=location)
        db.session.add(new_admin)
        db.session.commit()

        meal_name = "katogo"
        price = 3000
        process_status = "Pending"
        user_id = 1
        order = Orders(meal_name=meal_name, price=price, user_id=user_id,\
         process_status=process_status)
        db.session.add(order)
        db.session.commit()

        details = {
            "email": "steven@gmail.com", 
            "password": "54321"
        }
        response = self.app.post("/bookmealapi/v1.0/auth/login",\
            data=json.dumps(details), content_type='application/json')
        data = json.loads(response.get_data())
        token = data['token']

        response = self.app.delete('/bookmealapi/v1.0/orders/1',\
            headers={'x-access-token' : token})
        self.assertEqual(response.status_code, 200)

    def test_delete_menu_exists(self):
        """ Deleting a value that exists """
        business_name = "FAST FOOD"
        location = "nakulabye"
        first_name = "atlas"
        last_name = "waters"
        email = "steven@gmail.com"
        password = "54321"
        role_id = 1
        hashed_password = generate_password_hash(password, method='sha256')
        new_admin = User(first_name= first_name, last_name=last_name,\
                      email=email, password= hashed_password, role_id=role_id,\
                      business_name=business_name, location=location)
        db.session.add(new_admin)
        db.session.commit()

        meal_ids =[6, 2, 7, 4]
        meal_ids_string = ""
        for ids in meal_ids:
            meal_ids_string += ';%s' % ids 
        user_id = 1
        menu = Menu(user_id=user_id, meal_ids=meal_ids_string)
        db.session.add(menu)
        db.session.commit()

        details = {
            "email": "steven@gmail.com", 
            "password": "54321"
        }
        response = self.app.post("/bookmealapi/v1.0/auth/login",\
            data=json.dumps(details), content_type='application/json')
        data = json.loads(response.get_data())
        token = data['token']

        response = self.app.delete('/bookmealapi/v1.0/menu/1',\
            headers={'x-access-token' : token})
        self.assertEqual(response.status_code, 200)  

    def test_delete_menu_non_existant_data(self):
        """ Deleting menu that doesnt exist """
        business_name = "FAST FOOD"
        location = "nakulabye"
        first_name = "atlas"
        last_name = "waters"
        email = "steven@gmail.com"
        password = "54321"
        role_id = 1
        hashed_password = generate_password_hash(password, method='sha256')
        new_admin = User(first_name= first_name, last_name=last_name,\
                      email=email, password= hashed_password, role_id=role_id,\
                      business_name=business_name, location=location)
        db.session.add(new_admin)
        db.session.commit()

        details = {
            "email": "steven@gmail.com", 
            "password": "54321"
        }
        response = self.app.post("/bookmealapi/v1.0/auth/login",\
            data=json.dumps(details), content_type='application/json')
        data = json.loads(response.get_data())
        token = data['token']

        response = self.app.delete('/bookmealapi/v1.0/menu/10',\
            headers={'x-access-token' : token})
        self.assertEqual(response.status_code, 404)       

if __name__ == '__main__':
    unittest.main()
