import datetime

meals = [
    {
        'id': 1,
        'meal_name': "ricebeans",
        'price': 3000,
        'meal_type': "lunch",
        'availability': 0,
        'created_at': 'Fri, 04 May 2018 00:10:06 GMT',
        'updated_at': 'Fri, 04 May 2018 00:10:06 GMT'
    },
    {
        'id': 2,
        'meal_name': 'rolex',
        'price': 4000,
        'meal_type': 'lunch',
        'availability': 0,
        'created_at': 'Fri, 04 May 2018 00:10:06 GMT',
        'updated_at': 'Fri, 04 May 2018 00:10:06 GMT'
    }
]

class Meals():
    def __init__(self):
        self.meals = meals
        self.counter = 0

    def add_meals(self, data):
        meal_add = data
        for meal in self.meals:
            if meal["meal_name"] == meal_add['meal_name']:
                return "Meal Name Exists"
        if len(self.meals) == 0:
            new_id = 1
        else:    
            new_id = self.meals[-1].get("id") + 1
        meal_add['id'] = new_id
        meal_add['created_at'] = datetime.datetime.now()
        meal_add['updated_at'] = datetime.datetime.now()
        meal_add['availability'] = 0
        self.meals.append(meal_add)
        return "Successfully Added Meal"

    def get_meals(self, value):
        for meal in self.meals:
            if meal['id'] == value:
                return meal
        return "No Meals Found"

    def get_all_meals(self):
        return self.meals
                

    """ Test Case for this """
    def get_meals_name(self, value):
        for meal in self.meals:
            if meal['meal_name'] == value:
                return meal
        return "No Meals Found"    

    def remove_meals(self, value):
        for meals in self.meals:
            if meals['id'] == value:
                self.meals.remove(meals)
                return "Successfully Removed"
        return "No meals Found"

    def update_meals(self, value, data):
        meal = self.get_meals(value)
        meal['updated_at'] = datetime.datetime.now()
        meal['meal_name'] = data['meal_name']
        meal['price'] = data['price']
        meal['meal_type'] = data['meal_type']
        return meal

    def update_meals_availability(self, value):
        meal = self.get_meals_name(value)
        meal['updated_at'] = datetime.datetime.now()
        meal['availability'] = 1
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

    def menu_meals(self):
        output = []
        for meal in self.meals:
            if meal['availability'] == 1:
                output.append(meal)
        return output

    
