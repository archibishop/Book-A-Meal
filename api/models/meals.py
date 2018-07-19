import datetime
from .data import Data

class Meals():
    def __init__(self, meal_name, price, meal_type, availability):
        self.meal_name = meal_name
        self.price = price
        self.meal_type = meal_type
        self.availability = availability
        if len(Data.meals) > 0:
            id = Data.meals[-1].id + 1
        else:
            id = 1
        self.id = id

        

    def add_meals(self):
        Data.meals.append(self)
        return "Successfully Added Meal"

    @staticmethod
    def get_meals(value):
        
        for meal in Data.meals:
            if meal.id == value:
                return meal
        return "No Meals Found"

    @staticmethod
    def get_all_meals():
        return Data.meals
                

    """ Test Case for this """
    @staticmethod
    def get_meals_name(value):
        for meal in Data.meals:
            if meal.meal_name == value:
                return meal
        return "No Meals Found"    

    @staticmethod
    def remove_meals(value):
        for meals in Data.meals:
            if meals.id == value:
                Data.meals.remove(meals)
                return "Successfully Removed"
        return "No meals Found"

    @staticmethod
    def update_meals(value, data):
        meal = Meals.get_meals(value)
        meal.updated_at = datetime.datetime.now()
        meal.meal_name = data['meal_name']
        meal.price = data['price']
        meal.meal_type = data['meal_type']
        return meal

    def update_meals_availability(self, value):
        meal = Meals.get_meals_name(value)
        meal.updated_at = datetime.datetime.now()
        meal.availability = 1
        return meal

    @staticmethod
    def menu_meals(self):
        output = []
        for meal in Data.meals:
            if meal.availability == 1:
                output.append(meal)
        return output

    @staticmethod
    def meal_exists(mealname):
        for meal in Data.meals:
            if meal.meal_name == mealname:
                return True
        return False

    def validate(self):
        message, validation = '', True
        if self.meal_name is None or self.price is None or\
            self.meal_type is None:
            message, validation = "Missing Values in Data Sent", False
        elif self.meal_name.strip() == '' or self.meal_type.strip() == '':
            message, validation = "You sent some empty strings", False
        elif type(self.price) is not int:
            message, validation = "Price Should be Integer", False
        elif self.meal_exists(self.meal_name):
            message, validation = "Meal Name Exists", False
        if not validation:
            return message    
        return "Valid Data Sent"

    @staticmethod 
    def validate_json(data):
        message, validation = '', True 
        if data is None:
            message, validation = "No Data Sent", False
        elif 'meal_name' not in data or 'price' not in data \
            or 'meal_type' not in data:
            message, validation = "Missing Values in Data Sent", False
        elif data.get('meal_name') == '' or data.get('price') == ''\
            or data.get('meal_type') == '':
            message, validation = "You sent some empty strings", False
        elif type(data.get('price')) is not int:
            message, validation = "Price Should be Integer", False  
        if not validation:
            return message    
        return "Valid Data Sent" 

    
