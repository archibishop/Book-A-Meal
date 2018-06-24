"""import context """
from app import app
import unittest
import json
from models.admin import Admin
from models.order import Order
from models.user import User
from models.menu import Menu
from models.meals import Meals



BASE_URL = 'http://127.0.0.1:5000/bookmealapi/v1.0/meals/'


class api_test_case(unittest.TestCase):
    update_details = {
        "meal_ids": [6, 2, 7, 4],
        "user_id": 3
    }
    
    def setUp(self):
        self.app = app.test_client()

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
            "fname": "felix",
            "lname": "craig", 
            "email": "felix@gmail.com",
            "password": "12345"
        }
        response = self.app.post("/bookmealapi/v1.0/auth/signup",\
            data=json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data())
        self.assertEqual(data['user']['id'], 2)
        self.assertEqual(data['user']['first_name'], "felix")
        self.assertEqual(data['user']['last_name'], "craig")
        self.assertEqual(data['user']['email'], "felix@gmail.com")
        self.assertEqual(data['user']['password'], "12345")

        """ cannot add item with same email again """
        user = {
            "fname": "felix", 
            "lname": "craig",
            "email": "felix@gmail.com",
            "password": "12345"
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
        """ correct details """
        user = {
            "fname": "atlas",
            "lname": "red",
            "email": "atlas@gmail.com",
            "password": "12345"
        }
        response = self.app.post("/bookmealapi/v1.0/auth/signup",
            data=json.dumps(user), content_type='application/json')

        details = {
            "email": "atlas@gmail.com",
            "password": "12345"
        }
        response = self.app.post("/bookmealapi/v1.0/auth/login",\
            data=json.dumps(details), content_type='application/json')
        data = json.loads(response.get_data())
        # self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], "Successfully login")

    def test_login_valid_details_user2(self):
        """ correct details """
        user = {
            "fname": "atlas",
            "lname": "red",
            "email": "atlas@gmail.com",
            "password": "12345"
        }
        response = self.app.post("/bookmealapi/v1.0/auth/signup",
            data=json.dumps(user), content_type='application/json')

        details = {
            "email": "atlas@gmail.com",
            "password": "12345"
        }
        response = self.app.post("/bookmealapi/v1.0/auth/login",\
            data=json.dumps(details), content_type='application/json')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], "Successfully login")

    def test_login_valid_details_admin(self):
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
        self.assertEqual(response.status_code, 400)
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
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], "User Not Found")

    def test_add_meal(self):
        """ missing values """

        admin = Admin("Fast Foods", "steven", "lule",
                      "steven@gmail.com", "54321")
        admin.add_admin()
        
        self.login()

        details = {
            "mealname": "katogo"
        }
        response = self.app.post(
            "/bookmealapi/v1.0/meals", data=json.dumps(details), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_add_meal_price_is_string(self):
        """ # price cannot take string """

        self.login()

        details = {
            "mealname": "katogo", 
            "price": "2000", 
            "meal_type": "breakfast"
        }
        response = self.app.post("/bookmealapi/v1.0/meals",\
            data=json.dumps(details), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_add_meal_valid(self):
        """ correct values """
        self.login()

        details = {
            "meal_name": "katogo", 
            "price": 2000, 
            "meal_type": "breakfast"
        }
        response = self.app.post("/bookmealapi/v1.0/meals",\
            data=json.dumps(details), content_type='application/json')
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
            data=json.dumps(details), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_select_meal_missing_values(self):
        """  Mising Values in json """

        self.login()

        details = {
            "meal_name": "katogo"
        }
        response = self.app.post("/bookmealapi/v1.0/orders",
                                 data=json.dumps(details), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_select_meal_price_user_id_string(self):
        """  Price and userId cannot be string """
        self.login()

        details = {
            "meal_name": "katogo",
            "price": "2000", 
            "userId": "2"
        }
        response = self.app.post("/bookmealapi/v1.0/orders",\
            data=json.dumps(details), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_select_meal_valid(self):
        """  valid json """
        self.login()  

        details = {
            "meal_name": "katogo", 
            "price": 2000, 
            "userId": 2
        }
        response = self.app.post("/bookmealapi/v1.0/orders",\
            data=json.dumps(details), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_set_menu(self):
        """ setting the menu """
        self.login()

        details = {
            "meal_ids": [1, 2, 3, 4],
            "user_id": 2
        }
        response = self.app.post("/bookmealapi/v1.0/menu",
                                 data=json.dumps(details), content_type='application/json')
        data =  json.loads(response.get_data())   
        print(len(data['message']))                     
        self.assertEqual(response.status_code, 201)

    def test_delete_meal_option_non_existant_data(self):
        """ Deleting a value that doesnt exist """
        self.login()

        response = self.app.delete('/bookmealapi/v1.0/meals/10')
        self.assertEqual(response.status_code, 404)

    def test_delete_meal_option_data_exists(self):
        """ Deleting a value that exists """
        self.login()

        response = self.app.delete('/bookmealapi/v1.0/meals/1')
        self.assertEqual(response.status_code, 200)
    

    def test_update_meal_option(self):
        """ # missing values """
        self.login()

        details = {
            "meal_name": "katogo"
        }
        response = self.app.put("/bookmealapi/v1.0/meals/2",\
            data=json.dumps(details), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_update_meal_option_price_string(self):
        """ Price cannot be string """
        self.login()

        details = {
            "meal_name": "katogo", 
            "price": "8000"
        }
        response = self.app.put("/bookmealapi/v1.0/meals/1",\
            data=json.dumps(details), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_update_meal_option_valid(self):
        """ correct values """
        self.login()

        meal = Meals("rice", 2000, "lunch", 0)    
        meal.add_meals()

        details = {
            "meal_name": "rolex", 
            "price": 8000, 
            "meal_type": "breakfast"
        }
        response = self.app.put("/bookmealapi/v1.0/meals/1",\
            data=json.dumps(details), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data())
        self.assertEqual(data['meal']['meal_name'], "rolex")
        self.assertEqual(data['meal']['price'], 8000)
        self.assertEqual(data['meal']['meal_type'], "breakfast")

    def test_update_order_missing_values(self):
        """ Missing valuesvin json """
        self.login()

        details = {
            "meal_name": 
            "katogo"
        }
        response = self.app.put("/bookmealapi/v1.0/orders/2",\
                                data=json.dumps(details), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_update_order_price_string(self):
        """  Price cannot be string """
        self.login()

        details = {
            "meal_name": "katogo", 
            "price": "8000"
        }
        response = self.app.put("/bookmealapi/v1.0/orders/2",\
                                data=json.dumps(details), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_update_order_valid(self):
        """ Update Order """
        
        meal = Meals("rice", 2000, "breakfast", 0)
        meal.add_meals()

        order = Order("rice", 2000, 1) 
        order.place_order()  

        self.login()

        details = {
            "meal_name": "katogo",
            "price": 8000
        }
        response = self.app.put("/bookmealapi/v1.0/orders/1",
                                data=json.dumps(details), content_type='application/json')
        # self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data())
        # self.assertEqual(data['order']['id'], 2)
        self.assertEqual(data['order']['meal_name'], "katogo")
        self.assertEqual(data['order']['price'], 8000)

    def test_update_menu_missing_value(self):
        """ Incomplete json sent """
        self.login()
        details = {
            "user_id": 3
        }
        response = self.app.put("/bookmealapi/v1.0/menu/1",
                                data=json.dumps(details), content_type='application/json')
        self.assertEqual(response.status_code, 400) 

    
    def test_update_menu_nonexistant(self):
        """ Incomplete json sent """
        self.login()
        response = self.app.put("/bookmealapi/v1.0/menu/10",
                    data=json.dumps(api_test_case.update_details), content_type='application/json')
        self.assertEqual(response.status_code, 404) 
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], "Menu Does Not Exist")     

    def test_update_menu_valid(self):
        """ Update Menu """
        self.login()
        response = self.app.put("/bookmealapi/v1.0/menu/1",
                    data=json.dumps(api_test_case.update_details), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data())
        self.assertEqual(data['menu']['meal_ids'], [6, 2, 7, 4])
        

    def test_get_all_meals(self):
        """ Get all meals """
        self.login()
        
        meal = Meals("rice", 2000, "breakfast", 0)
        meal.add_meals()

        response = self.app.get('/bookmealapi/v1.0/meals')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['meals']), 1)

    def test_get_all_orders(self):
        """ Get All orders """
        self.login()

        order = Order("rice", 3000, 2)  
        order.place_order()  

        response = self.app.get('/bookmealapi/v1.0/orders')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['transactions']),1)

    def test_get_menu_day(self):
        """ Get menu  for the day """
        menu = Menu([1,4], 2)
        menu.add_meals_menu()

        self.login()

        response = self.app.get('/bookmealapi/v1.0/menu')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['menu_day']), 1)

    def test_delete_order_non_existant_data(self):
        """ Deleting order that doesnt exist """
        self.login()

        response = self.app.delete('/bookmealapi/v1.0/orders/10')
        self.assertEqual(response.status_code, 404)

    
    def test_delete_order_data_exists(self):
        """ Deleting an order """
        order = Order("rice", 2000, 1)
        order.place_order()

        details = {
            "email": "steven@gmail.com", 
            "password": "54321"
        }
        response = self.app.post("/bookmealapi/v1.0/auth/login",\
            data=json.dumps(details), content_type='application/json')

        response = self.app.delete('/bookmealapi/v1.0/orders/1')
        self.assertEqual(response.status_code, 200)

    def test_delete_menu_exists(self):
        """ Deleting a value that exists """

        menu = Menu([1,2], 3)
        menu.add_meals_menu()

        self.login()

        response = self.app.delete('/bookmealapi/v1.0/menu/1')
        self.assertEqual(response.status_code, 200)  

    def test_delete_menu_non_existant_data(self):
        """ Deleting menu that doesnt exist """
        self.login()

        response = self.app.delete('/bookmealapi/v1.0/menu/10')
        self.assertEqual(response.status_code, 404)  

    def login(self):
        details = {
            "email": "steven@gmail.com",
            "password": "54321"
        }
        response = self.app.post("/bookmealapi/v1.0/auth/login",
            data=json.dumps(details), content_type='application/json')
        data = json.loads(response.get_data())

if __name__ == '__main__':
    unittest.main()
