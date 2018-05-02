import datetime


class Meals():
    def __init__(self):
        self.meals = []
        self.counter = 0

    def add_meals(self, data):
        meals = data
        self.counter = self.counter + 1
        meals['id'] = self.counter
        meals['created_at'] = datetime.datetime.now()
        meals['updated_at'] = datetime.datetime.now()
        self.meals.append(meals)
        return "Successfully Added"

    def get_meals(self, value):
        for meals in self.meals:
            if meals['id'] == value:
                return meals
        return "No Meals Found"

    def remove_meals(self, value):
        for meals in self.meals:
            if meals['id'] == value:
                self.meals.remove(meals)
                return "Successfully Removed"
        return "No meals Found"

    def update_meals(self, value, data):
        meals = self.get_meals(value)
        meals['updated_at'] = datetime.datetime.now()
        meals = data
        return meals
