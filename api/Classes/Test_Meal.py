import unittest

from Meals import Meals

class TestMeals(unittest.TestCase):
    def test_add_Meals(self):
        meals = Meals()
        data = {
           "mealname": "katogo",
           "type": "brakfast",
           "availability": 0,
        }
        self.assertEqual(meals.addMeals(data), "Successfully Added")

    def test_get_Meals(self):
        meals = Meals()
        data1 = {
           "mealname": "ricebeans",
           "type": "lunch",
           "availability": 0,
        }
        data2 = {
           "mealname": "rolex",
           "type": "supper",
           "availability": 0,
        }
      
        self.assertEqual(meals.addMeals(data1), "Successfully Added")
        self.assertEqual(meals.addMeals(data2), "Successfully Added")
        self.assertEqual(meals.getMeals(2), data2)    
        self.assertEqual(meals.getMeals(1), data1)
        self.assertEqual(meals.getMeals(3), "No Meals Found")  
            

    def test_remove_meals(self):
        meals = Meals()
        data1 = {
           "mealname": "ricebeans",
           "type": "lunch",
           "availability": 0,
        }
        data2 = {
           "mealname": "rolex",
           "type": "supper",
           "availability": 0,
        }
        self.assertEqual(meals.addMeals(data1), "Successfully Added")
        self.assertEqual(meals.addMeals(data2), "Successfully Added")
        self.assertEqual(meals.removeMeals(1), "Successfully Removed")   
        self.assertEqual(meals.getMeals(1), "No Meals Found")
        self.assertEqual(meals.getMeals(2), data2)

    def test_update_meals(self):
        meals = Meals()
        data1 = {
           "mealname": "ricebeans",
           "type": "lunch",
           "availability": 0,
        }
        data2 = {
           "mealname": "rolex",
           "type": "supper",
           "availability": 0,
        }
        self.assertEqual(meals.addMeals(data1), "Successfully Added")  
        self.assertEqual(meals.updateMeals(1, data2), data2)


    def test_set_availabilty(self):
        meals = Meals()
        data1 = {
           "availability": 1,
        }
        self.assertEqual(meals.addMeals(data1), "Successfully Added")  
        self.assertEqual(meals.updateMeals(1, data1), data1)    
        


if __name__ == '__main__':
    unittest.main()    