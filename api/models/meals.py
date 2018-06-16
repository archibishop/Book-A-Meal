import datetime
from .data import Data

# meals = [
#     {
#         'id': 1,
#         'meal_name': "ricebeans",
#         'price': 3000,
#         'meal_type': "lunch",
#         'availability': 0,
#         'created_at': 'Fri, 04 May 2018 00:10:06 GMT',
#         'updated_at': 'Fri, 04 May 2018 00:10:06 GMT'
#     },
#     {
#         'id': 2,
#         'meal_name': 'rolex',
#         'price': 4000,
#         'meal_type': 'lunch',
#         'availability': 0,
#         'created_at': 'Fri, 04 May 2018 00:10:06 GMT',
#         'updated_at': 'Fri, 04 May 2018 00:10:06 GMT'
#     }
# ]

class Meals():
    def __init__(self, meal_name, price, meal_type, availability):
        # self.meals = meals
        # self.counter = 0
        self.meal_name = meal_name
        self.price = price
        self.meal_type = meal_type
        self.availability = availability
        id = len(Data.meals) + 1
        self.id = len(Data.meals) + 1

        

    def add_meals(self):
        for meal in Data.meals:
            if meal.meal_name == self.meal_name:
                return "Meal Name Exists"
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

    def remove_meal_menu(self, value):
        """ for meal in self.meals:
             if meal['availability'] == 1:
                 if meal[]
         meal = self.get_meals(value)
        You should use the meal name to delte
         if meal == "No Meals Found":
             return "No Meals Found"  
         else:
             meal['availability'] = 0 
             return meal """

    @staticmethod
    def menu_meals(self):
        output = []
        for meal in Data.meals:
            if meal.availability == 1:
                output.append(meal)
        return output

    
