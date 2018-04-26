import unittest

from User import User


class TestUser(unittest.TestCase):
    def test_add_user(self):
        user = User()
        data = {
            "firstname": "craig",
            "lastname": "red",
            "email": "craig@gmail.com",
            "password": "1234"
        }
        self.assertEqual(user.addUser(data), "Successfully Added")

    def test_get_user(self):
        user = User()
        data1 = {
            "firstname": "craig",
            "lastname": "red",
            "email": "craig@gmail.com",
            "password": "54321"
        }
        data2 = {
            "firstname": "drink",
            "lastname": "water",
            "email": "drinkwater@gmail.com",
            "password": "12345"
        }
        data3 = {
            "firstname": "guest",
            "lastname": "lap",
            "email": "lap@gmail.com",
            "password": "12233"
        }
        self.assertEqual(user.addUser(data1), "Successfully Added")
        self.assertEqual(user.addUser(data2), "Successfully Added")
        self.assertEqual(user.addUser(data3), "Successfully Added")
        self.assertEqual(user.getUser(2), data2)
        self.assertEqual(user.getUser(1), data1)
        self.assertEqual(user.getUser(3), data3)
        self.assertEqual(user.getUser(6), "No User Found")

    def test_get_all_user(self):
        user = User()
        test = []
        data1 = {
            "firstname": "craig",
            "lastname": "red",
            "email": "craig@gmail.com",
            "password": "54321"
        }
        data2 = {
            "firstname": "drink",
            "lastname": "water",
            "email": "drinkwater@gmail.com",
            "password": "12345"
        }
        data3 = {
            "firstname": "guest",
            "lastname": "lap",
            "email": "lap@gmail.com",
            "password": "12233"
        }
        test.append(data1)
        test.append(data2)
        test.append(data3)
        self.assertEqual(user.addUser(data1), "Successfully Added")
        self.assertEqual(user.addUser(data2), "Successfully Added")
        self.assertEqual(len(user.getAllUsers()), 2)
        self.assertEqual(user.addUser(data3), "Successfully Added")
        self.assertEqual(len(user.getAllUsers()), 3)
        self.assertEqual((user.getAllUsers()), test)

    def test_remove_user(self):
        user = User()
        data1 = {
            "firstname": "craig",
            "lastname": "red",
            "email": "craig@gmail.com",
            "password": "1234"
        }
        data2 = {
            "firstname": "drink",
            "lastname": "water",
            "email": "drinkwater@gmail.com",
            "password": "1234"
        }
        self.assertEqual(user.addUser(data1), "Successfully Added")
        self.assertEqual(user.addUser(data2), "Successfully Added")
        self.assertEqual(user.removeUser(1), "Successfully Removed")
        self.assertEqual(user.getUser(1), "No User Found")
        self.assertEqual(user.getUser(2), data2)

    def test_update_user(self):
        user = User()
        data1 = {
            "firstname": "craig",
            "lastname": "red",
            "email": "craig@gmail.com",
            "password": "1234"
        }
        data2 = {
            "firstname": "drink",
            "lastname": "water",
            "email": "drinkwater@gmail.com",
            "password": "1234"
        }
        self.assertEqual(user.addUser(data1), "Successfully Added")
        self.assertEqual(user.updateUser(1, data2), data2)


if __name__ == '__main__':
    unittest.main()
