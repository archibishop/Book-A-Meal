import unittest

from meals import Meals


class meal_tests(unittest.TestCase):
    def test_add_Meals(self):
        meals = Meals()
        data = {
            "mealname": "katogo",
            "type": "brakfast",
            "availability": 0,
        }
        self.assertEqual(meals.add_meals(data), "Successfully Added")

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

        self.assertEqual(meals.add_meals(data1), "Successfully Added")
        self.assertEqual(meals.add_meals(data2), "Successfully Added")
        self.assertEqual(meals.get_meals(2), data2)
        self.assertEqual(meals.get_meals(1), data1)
        self.assertEqual(meals.get_meals(3), "No Meals Found")

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
        self.assertEqual(meals.add_meals(data1), "Successfully Added")
        self.assertEqual(meals.add_meals(data2), "Successfully Added")
        self.assertEqual(meals.remove_meals(1), "Successfully Removed")
        self.assertEqual(meals.get_meals(1), "No Meals Found")
        self.assertEqual(meals.get_meals(2), data2)

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
        self.assertEqual(meals.add_meals(data1), "Successfully Added")
        self.assertEqual(meals.update_meals(1, data2), data2)

    def test_set_availabilty(self):
        meals = Meals()
        data1 = {
            "availability": 1,
        }
        self.assertEqual(meals.add_meals(data1), "Successfully Added")
        self.assertEqual(meals.update_meals(1, data1), data1)


if __name__ == '__main__':
    unittest.main()
