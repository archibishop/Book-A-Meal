import unittest

from Order import Order


class TestOrder(unittest.TestCase):
    def test_add_order(self):
        order = Order()
        data = {
            "id": 1,
            "mealId": 1,
            "customerId": 2,
            "price": 2000,
        }
        self.assertEqual(order.placeOrder(data), "Successfully Made Order")

    def test_get_order(self):
        order = Order()
        data1 = {
            "id": 1,
            "mealId": 1,
            "customerId": 2,
            "price": 2000,
        }
        data2 = {
            "id": 2,
            "mealId": 1,
            "customerId": 3,
            "price": 4000,
        }

        self.assertEqual(order.placeOrder(data1), "Successfully Made Order")
        self.assertEqual(order.placeOrder(data2), "Successfully Made Order")
        self.assertEqual(order.getOrder(2), data2)
        self.assertEqual(order.getOrder(1), data1)
        self.assertEqual(order.getOrder(3), "No Order Found")

    def test_get_order_users(self):
        order = Order()
        data1 = {
            "id": 1,
            "mealId": 1,
            "customerId": 2,
            "price": 2000,
        }
        data2 = {
            "id": 2,
            "mealId": 1,
            "customerId": 3,
            "price": 4000,
        }
        data3 = {
            "id": 2,
            "mealId": 1,
            "customerId": 2,
            "price": 4000,
        }

        self.assertEqual(order.placeOrder(data1), "Successfully Made Order")
        self.assertEqual(order.placeOrder(data2), "Successfully Made Order")
        self.assertEqual(order.placeOrder(data3), "Successfully Made Order")
        self.assertEqual(len(order.getOrdersUser(2)), 2)
        self.assertEqual(len(order.getOrdersUser(3)), 1)
        self.assertEqual(len(order.getOrdersUser(10)), 0)    

    def test_remove_order(self):
        order = Order()
        data1 = {
            "id": 1,
            "mealId": 1,
            "customerId": 2,
            "price": 2000,
        }
        data2 = {
            "id": 2,
            "mealId": 1,
            "customerId": 3,
            "price": 4000,
        }
        self.assertEqual(order.placeOrder(data1), "Successfully Made Order")
        self.assertEqual(order.placeOrder(data2), "Successfully Made Order")
        self.assertEqual(order.removeOrder(1), "Successfully Removed")
        self.assertEqual(order.getOrder(1), "No Order Found")
        self.assertEqual(order.getOrder(2), data2)

    def test_update_order(self):
        order = Order()
        data1 = {
            "id": 1,
            "mealId": 1,
            "customerId": 2,
            "price": 2000,
        }
        data2 = {
            "id": 2,
            "mealId": 1,
            "customerId": 3,
            "price": 4000,
        }
        self.assertEqual(order.placeOrder(data1), "Successfully Made Order")
        self.assertEqual(order.updateOrder(1, data2), data2)


if __name__ == '__main__':
    unittest.main()
