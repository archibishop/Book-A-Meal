import unittest

import context

from models.user import User


class user_tests(unittest.TestCase):
    def test_add_user(self):
        user1 = User()
        data = {
            "firstname": "craig",
            "lastname": "red",
            "email": "test@gmail.com",
            "password": "1234"
        }
        self.assertEqual(user1.add_user(data)['email'], "test@gmail.com")

    def test_get_user(self):
        user1 = User()
        data = {
            "firstname": "craig",
            "lastname": "red",
            "email": "test@gmail.com",
            "password": "1234"
        }
        self.assertEqual(user1.get_user(3)['email'], data['email'])
        self.assertEqual(user1.get_user(6), "No User Found")

    def test_get_all_user(self):
        user1 = User()
        self.assertEqual(len(user1.get_all_users()), 3)

    def test_remove_user(self):
        user1 = User()
        self.assertEqual(user1.remove_user(1), "Successfully Removed")
        self.assertEqual(user1.get_user(1), "No User Found")

    def test_update_user(self):
        user1 = User()
        data2 = {
            "firstname": "drink",
            "lastname": "water",
            "email": "drinkwater@gmail.com",
            "password": "1234"
        }
        self.assertEqual(user1.update_user(3, data2)['email'], "drinkwater@gmail.com")


if __name__ == '__main__':
    unittest.main()
