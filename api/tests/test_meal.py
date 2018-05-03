import unittest

import context

from models.meals import Meals


class meal_tests(unittest.TestCase):
    def test_add_Meals(self):
        meals1 = Meals()
        data = {
            "meal_name": "katogo",
            "meal_type": "brakfast",
            "availability": 0,
        }
        self.assertEqual(meals1.add_meals(data), "Successfully Added Meal")

    def test_get_Meals(self):
        meals1 = Meals()
        data1 = {
            "meal_name": "cassava",
            "meal_type": "lunch",
            "availability": 0,
        }
        data2 = {
            "meal_name": "nyana mbisi",
            "meal_type": "supper",
            "availability": 0,
        }

        self.assertEqual(meals1.add_meals(data1), "Successfully Added Meal")
        self.assertEqual(meals1.add_meals(data2), "Successfully Added Meal")
        self.assertEqual(meals1.get_meals(5), data2)
        self.assertEqual(meals1.get_meals(4), data1)
        self.assertEqual(meals1.get_meals(6), "No Meals Found")

    def test_remove_meals(self):
        meals1 = Meals()
        self.assertEqual(meals1.remove_meals(1), "Successfully Removed")
        self.assertEqual(meals1.get_meals(1), "No Meals Found")

    def test_update_meals(self):
        meals1 = Meals()
        data1 = {
            "meal_name": "spinach",
            "meal_type": "lunch",
            "price": 5000,
        }
        self.assertEqual(meals1.add_meals(data1), "Successfully Added Meal")
        self.assertEqual(meals1.update_meals(3, data1)['meal_name'],\
         data1['meal_name'])

    def test_set_availabilty(self):
        meals1 = Meals()
        data1 = {
            "meal_name": "cassava",
        }
        self.assertEqual(meals1.update_meals_availability\
            (data1['meal_name'])['availability'], 1)


if __name__ == '__main__':
    unittest.main()
