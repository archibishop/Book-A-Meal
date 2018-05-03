import unittest

import context

from models.user import User


class user_tests(unittest.TestCase):
    def test_add_user(self):
        user = User()
        data = {
            "firstname": "craig",
            "lastname": "red",
            "email": "test@gmail.com",
            "password": "1234"
        }
        self.assertEqual(user.add_user(data)['email'], "test@gmail.com")

    def test_get_user(self):
        user = User()
        data = {
            "firstname": "craig",
            "lastname": "red",
            "email": "test@gmail.com",
            "password": "1234"
        }
        
        # self.assertEqual(user.add_user(data1), "Successfully Added")
        # self.assertEqual(user.add_user(data2), "Successfully Added")
        self.assertEqual(user.get_user(3)['email'], data['email'])
        # self.assertEqual(user.get_user(1), data1)
        self.assertEqual(user.get_user(6), "No User Found")

    def test_get_all_user(self):
        user = User()
        # test = []
        # data1 = {
        #     "firstname": "craig",
        #     "lastname": "red",
        #     "email": "craig@gmail.com",
        #     "password": "54321"
        # }
        # data2 = {
        #     "firstname": "drink",
        #     "lastname": "water",
        #     "email": "drinkwater@gmail.com",
        #     "password": "12345"
        # }
        # data3 = {
        #     "firstname": "guest",
        #     "lastname": "lap",
        #     "email": "lap@gmail.com",
        #     "password": "12233"
        # }
        # test.append(data1)
        # test.append(data2)
        # test.append(data3)
        # self.assertEqual(user.add_user(data1), "Successfully Added")
        # self.assertEqual(user.add_user(data2), "Successfully Added")
        self.assertEqual(len(user.get_all_users()), 3)
        # self.assertEqual(user.add_user(data3), "Successfully Added")
        # self.assertEqual(len(user.get_all_users()), 3)
        # self.assertEqual((user.get_all_users()), test)

    def test_remove_user(self):
        user = User()
        # data1 = {
        #     "firstname": "craig",
        #     "lastname": "red",
        #     "email": "craig@gmail.com",
        #     "password": "1234"
        # }
        # data2 = {
        #     "firstname": "drink",
        #     "lastname": "water",
        #     "email": "drinkwater@gmail.com",
        #     "password": "1234"
        # }
        # self.assertEqual(user.add_user(data1), "Successfully Added")
        # self.assertEqual(user.add_user(data2), "Successfully Added")
        self.assertEqual(user.remove_user(1), "Successfully Removed")
        self.assertEqual(user.get_user(1), "No User Found")
        # self.assertEqual(user.get_user(2), data2)

    def test_update_user(self):
        user = User()
        data2 = {
            "firstname": "drink",
            "lastname": "water",
            "email": "drinkwater@gmail.com",
            "password": "1234"
        }

        self.assertEqual(user.update_user(3, data2)['email'], "drinkwater@gmail.com")


if __name__ == '__main__':
    unittest.main()
