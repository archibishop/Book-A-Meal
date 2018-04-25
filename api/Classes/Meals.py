import datetime

class Meals():
    def __init__(self):
        self.meals = []
        self.counter = 0

    def addMeals(self, data):
        meals = data
        self.counter =  self.counter + 1
        meals['id'] = self.counter
        meals['created_at'] = datetime.datetime.now()
        meals['updated_at'] = datetime.datetime.now()
        self.meals.append(meals)
        return "Successfully Added"

    def getMeals(self, value):
        for meals in self.meals:
            if meals['id'] == value:
                return meals
        return "No Meals Found"   

    def removeMeals(self, value):
        for meals in self.meals:
            if meals['id'] == value:
                self.meals.remove(meals)
                return "Successfully Removed"
        return "No meals Found"

    def updateMeals(self, value, data):
        meals = self.getMeals(value)
        meals['updated_at'] = datetime.datetime.now()
        meals = data 
        return meals


