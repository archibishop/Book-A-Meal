import unittest

from order import Order

import datetime


class order_tests(unittest.TestCase):
    def test_add_order(self):
        order = Order()
        data = {
            "id": 1,
            "mealId": 1,
            "customerId": 2,
            "price": 2000,
            "created_at": "2018-04-26 10:55:55.423844",
            "process_status":"pending"
        }
        self.assertEqual(order.place_order(data), "Successfully Made Order")

    def test_get_order(self):
        order = Order()
        data1 = {
            "id": 1,
            "mealId": 1,
            "customerId": 2,
            "price": 2000,
            "created_at": "2018-04-26 10:55:55.423844",
            "process_status":"pending"
        }
        data2 = {
            "id": 2,
            "mealId": 1,
            "customerId": 3,
            "price": 4000,
            "created_at": "2018-04-26 10:55:55.423844",
            "process_status":"pending"
        }

        self.assertEqual(order.place_order(data1), "Successfully Made Order")
        self.assertEqual(order.place_order(data2), "Successfully Made Order")
        self.assertEqual(order.get_order(2), data2)
        self.assertEqual(order.get_order(1), data1)
        self.assertEqual(order.get_order(3), "No Order Found")

    def test_get_order_users(self):
        order = Order()
        data1 = {
            "id": 1,
            "mealId": 1,
            "customerId": 2,
            "price": 2000,
            "created_at": "2018-04-26 10:55:55.423844",
            "process_status":"pending"
        }
        data2 = {
            "id": 2,
            "mealId": 1,
            "customerId": 3,
            "price": 4000,
            "created_at": "2018-04-26 10:55:55.423844",
            "process_status":"pending"
        }
        data3 = {
            "id": 2,
            "mealId": 1,
            "customerId": 2,
            "price": 4000,
            "created_at": "2018-04-26 10:55:55.423844",
            "process_status":"pending"
        }

        self.assertEqual(order.place_order(data1), "Successfully Made Order")
        self.assertEqual(order.place_order(data2), "Successfully Made Order")
        self.assertEqual(order.place_order(data3), "Successfully Made Order")
        self.assertEqual(len(order.get_orders_user(2)), 2)
        self.assertEqual(len(order.get_orders_user(3)), 1)
        self.assertEqual(len(order.get_orders_user(10)), 0)    

    def test_remove_order(self):
        order = Order()
        data1 = {
            "id": 1,
            "mealId": 1,
            "customerId": 2,
            "price": 2000,
            "created_at": "2018-04-26 10:55:55.423844",
            "process_status":"pending"
        }
        data2 = {
            "id": 2,
            "mealId": 1,
            "customerId": 3,
            "price": 4000,
            "created_at": "2018-04-26 10:55:55.423844",
            "process_status":"pending"
        }
        self.assertEqual(order.place_order(data1), "Successfully Made Order")
        self.assertEqual(order.place_order(data2), "Successfully Made Order")
        self.assertEqual(order.remove_order(1), "Successfully Removed")
        self.assertEqual(order.get_order(1), "No Order Found")
        self.assertEqual(order.get_order(2), data2)

    def test_update_order(self):
        order = Order()
        data1 = {
            "id": 1,
            "mealId": 1,
            "customerId": 2,
            "price": 2000,
            "created_at": "2018-04-26 10:55:55.423844",
            "process_status":"pending"
        }
        data2 = {
            "id": 2,
            "mealId": 1,
            "customerId": 3,
            "price": 4000,
            "created_at": "2018-04-26 10:55:55.423844",
            "process_status":"pending"
        }
        self.assertEqual(order.place_order(data1), "Successfully Made Order")
        self.assertEqual(order.update_order(1, data2), data2)

  


if __name__ == '__main__':
    unittest.main()
