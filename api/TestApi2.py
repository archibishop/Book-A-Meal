import os
from app import app
import unittest
import json

BASE_URL = 'http://127.0.0.1:5000/bookmealapi/v1.0/meals/'
UPDATE_ITEM_URL = '{}/2'.format(BASE_URL)
DELETE_ITEM_URL = '{}/1'.format(BASE_URL)


class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_signUp(self):

        # missing value in request sent
        user = {"fname" : "brian", "lname" : "Wagubi", "password":"12345"} 
        response = self.app.post("/bookmealapi/v1.0/auth/signup", data=json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 400)

        #valid add item but different password ad confirm password
        user = {"fname" : "brian", "lname" : "Wagubi", "email":"wagubib@gmail.com", "password":"45667","cnfmpassword":"12345"}
        response = self.app.post("/bookmealapi/v1.0/auth/signup", data=json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # valid add item, all fields avaiable
        user = {"fname" : "brian", "lname" : "Wagubi", "email":"wagubib@gmail.com", "password":"12345","cnfmpassword":"12345"}
        response = self.app.post("/bookmealapi/v1.0/auth/signup", data=json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data())
        self.assertEqual(data['user']['id'], 3)
        self.assertEqual(data['user']['firstname'], "brian")
        self.assertEqual(data['user']['lastname'], "Wagubi")
        self.assertEqual(data['user']['email'], "wagubib@gmail.com")
        self.assertEqual(data['user']['password'], "12345")

        # cannot add item with same email again
        user = {"fname" : "water", "lname" : "Wagubi", "email":"wagubib@gmail.com", "password":"12345","cnfmpassword":"12345"}
        response = self.app.post("/bookmealapi/v1.0/auth/signup", data=json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 400)   

    def test_login(self):
        # missing values
        details = {"email" : "wagubib@gmail.com"}
        response = self.app.post("/bookmealapi/v1.0/auth/login", data=json.dumps(details), content_type='application/json')
        self.assertEqual(response.status_code, 400) 


        # correct details
        details = {"email" : "lubega@gmail.com", "password":"12345"}
        response = self.app.post("/bookmealapi/v1.0/auth/login", data=json.dumps(details), content_type='application/json')
        self.assertEqual(response.status_code, 200) 
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], "Successfully login")

        # invalid details
        details = {"email" : "fresh@gmail.com", "password":"12345"}
        response = self.app.post("/bookmealapi/v1.0/auth/login", data=json.dumps(details), content_type='application/json')
        # self.assertEqual(response.status_code, 400) 
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], "User Not Found")

    def test_add_meal(self):
        #missing values
        details = {"mealname":"katogo"}
        response = self.app.post("/bookmealapi/v1.0/meals", data=json.dumps(details), content_type='application/json')
        self.assertEqual(response.status_code, 400)  

        # price cannot take string
        details = {"mealname":"katogo", "price": "2000", "type1":"breakfast"}
        response = self.app.post("/bookmealapi/v1.0/meals", data=json.dumps(details), content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # correct values
        details = {"mealname":"katogo", "price":2000, "type1":"breakfast"}
        response = self.app.post("/bookmealapi/v1.0/meals", data=json.dumps(details), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data())
        self.assertEqual(data['meal']['id'], 3)
        self.assertEqual(data['meal']['mealname'], "katogo")
        self.assertEqual(data['meal']['price'], 2000)
        self.assertEqual(data['meal']['type1'], "breakfast")

        # should not add meal with the same name
        details = {"mealname":"katogo", "price":2000, "type1":"breakfast"}
        response = self.app.post("/bookmealapi/v1.0/meals", data=json.dumps(details), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        

    def test_select_meal(self):
        #missing values
        details = {"mealname":"katogo"} 
        response = self.app.post("/bookmealapi/v1.0/orders", data=json.dumps(details), content_type='application/json')
        self.assertEqual(response.status_code, 400) 

        #Price and userId cannot be string
        details = {"mealname":"katogo", "price": "2000", "userId": "2"} 
        response = self.app.post("/bookmealapi/v1.0/orders", data=json.dumps(details), content_type='application/json')
        self.assertEqual(response.status_code, 400)

        #correct values
        details = {"mealname":"katogo", "price": 2000, "userId": 2} 
        response = self.app.post("/bookmealapi/v1.0/orders", data=json.dumps(details), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data())
        self.assertEqual(data['transaction']['id'], 4)
        self.assertEqual(data['transaction']['mealname'], "katogo")
        self.assertEqual(data['transaction']['price'], 2000)
        self.assertEqual(data['transaction']['user_id'], 2)  

        

    def test_set_menu(self):
        #correct values
        details = {"mealname":"katogo", "price": 2000} 
        response = self.app.post("/bookmealapi/v1.0/menu", data=json.dumps(details), content_type='application/json')
        self.assertEqual(response.status_code, 201)   

     

    def test_delete_meal_option(self):
        #Non existant value
        response = self.app.delete('/bookmealapi/v1.0/meals/10')
        self.assertEqual(response.status_code, 404)
        
        #Actual Value
        response = self.app.delete('/bookmealapi/v1.0/meals/1')
        self.assertEqual(response.status_code, 204)

    def test_update_meal_option(self): 
        #missing values
        details = {"mealname":"katogo"} 
        response = self.app.put("/bookmealapi/v1.0/meals/2", data=json.dumps(details), content_type='application/json')
        self.assertEqual(response.status_code, 400) 

        #Price cannot be string
        details = {"mealname":"katogo", "price": "8000"} 
        response = self.app.put("/bookmealapi/v1.0/meals/2", data=json.dumps(details), content_type='application/json')
        self.assertEqual(response.status_code, 400)


        #correct values 
        details = {"mealname":"katogo","price": 8000,"type1": "breakfast"} 
        response = self.app.put("/bookmealapi/v1.0/meals/2", data=json.dumps(details), content_type='application/json')
        self.assertEqual(response.status_code, 201)    
        data = json.loads(response.get_data())
        self.assertEqual(data['meal']['id'], 2)
        self.assertEqual(data['meal']['mealname'], "katogo") 
        self.assertEqual(data['meal']['price'], 8000)
        self.assertEqual(data['meal']['type1'], "breakfast")

    def test_update_order(self):
        #missing values
        details = {"mealname":"katogo"} 
        response = self.app.put("/bookmealapi/v1.0/orders/2", data=json.dumps(details), content_type='application/json')
        self.assertEqual(response.status_code, 400) 

        #Price cannot be string
        details = {"mealname":"katogo", "price": "8000"} 
        response = self.app.put("/bookmealapi/v1.0/orders/2", data=json.dumps(details), content_type='application/json')
        self.assertEqual(response.status_code, 400)

        #correct values  
        details = {"mealname":"katogo","price": 8000} 
        response = self.app.put("/bookmealapi/v1.0/orders/2", data=json.dumps(details), content_type='application/json')
        self.assertEqual(response.status_code, 201)    
        data = json.loads(response.get_data())
        self.assertEqual(data['transaction']['id'], 2)
        self.assertEqual(data['transaction']['mealname'], "katogo") 
        self.assertEqual(data['transaction']['price'], 8000)    

    def test_get_all_meals(self):
        response = self.app.get('/bookmealapi/v1.0/meals')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['meals']), 2)
    
    def test_get_all_orders(self):
        response = self.app.get('/bookmealapi/v1.0/orders')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['transactions']), 3)

    def test_get_menu_day(self):
        response = self.app.get('/bookmealapi/v1.0/menu')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['menuDay']), 4)
            

    
       
        
if __name__ == '__main__':
     unittest.main()       