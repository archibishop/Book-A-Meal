import unittest

# import context

from models.order import Order

import datetime


class order_tests(unittest.TestCase):
    def test_add_order(self):
        order1 = Order()
        data = {
            "id": 1,
            "mealId": 1,
            "user_id": 2,
            "price": 2000,
            "created_at": "2018-04-26 10:55:55.423844",
            "process_status":"pending"
        }
        self.assertEqual(order1.place_order(data), "Successfully Made Order")

    def test_get_order(self):
        order1 = Order()
        data1 = {
            "id": 1,
            "mealId": 1,
            "user_id": 2,
            "price": 2000,
            "created_at": "2018-04-26 10:55:55.423844",
            "process_status":"pending"
        }
        data2 = {
            "id": 2,
            "mealId": 1,
            "user_id": 3,
            "price": 4000,
            "created_at": "2018-04-26 10:55:55.423844",
            "process_status":"pending"
        }

        self.assertEqual(order1.place_order(data1), "Successfully Made Order")
        self.assertEqual(order1.place_order(data2), "Successfully Made Order")
        self.assertEqual(order1.get_order(6), data2)
        self.assertEqual(order1.get_order(5), data1)
        self.assertEqual(order1.get_order(7), "No Order Found")

    def test_get_order_users(self):
        order1 = Order()
        self.assertEqual(len(order1.get_orders_user(6)), 0)
        self.assertEqual(len(order1.get_orders_user(3)), 1)
        self.assertEqual(len(order1.get_orders_user(10)), 0)    

    def test_remove_order(self):
        order1 = Order()
        self.assertEqual(order1.remove_order(1), "Successfully Removed")
        self.assertEqual(order1.get_order(1), "No Order Found")


    def test_update_order(self):
        order1 = Order()
        data1 = {
            "id": 1,
            "meal_name": "eggs",
            "user_id": 2,
            "price": 2000,
            "created_at": "2018-04-26 10:55:55.423844",
            "process_status":"pending"
        }
        self.assertEqual(order1.update_order(5, data1)['meal_name'], "eggs")

  


if __name__ == '__main__':
    unittest.main()
