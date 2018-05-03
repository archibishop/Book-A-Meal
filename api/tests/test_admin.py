import unittest

import context

from models.admin import Admin


class admin_tests(unittest.TestCase):
    def test_add_admin(self):
        admin = Admin()
        data = {
            "business": "EAT FAST",
            "location": "Ntinda",
            "firstname": "phillip",
            "lastname": "owens",
            "email": "phillip@gmail.com",
            "password": "1234"
        }
        self.assertEqual(admin.add_admin(data), "Successfully Added")

    def test_get_admin(self):
        admin = Admin()
        data1 = {
            "business": "TRUST MEALS",
            "location": "Ntinda",
            "firstname": "phillip",
            "lastname": "owens",
            "email": "phillip@gmail.com",
            "password": "1234"
        }
        data2 = {
            "business": "SMILE FOOD",
            "location": "Kawempe",
            "firstname": "friend",
            "lastname": "stuart",
            "email": "pfriend@gmail.com",
            "password": "1234"
        }

        self.assertEqual(admin.add_admin(data1), "Successfully Added")
        self.assertEqual(admin.add_admin(data2), "Successfully Added")
        self.assertEqual(admin.get_admin(4), data2)
        self.assertEqual(admin.get_admin(3), data1)
        self.assertEqual(admin.get_admin(5), "No Admin Found")

    def test_remove_admin(self):
        admin = Admin()
        # data1 = {
        #     "business": "FAST MEALS",
        #     "location": "Ntinda",
        #     "firstname": "phillip",
        #     "lastname": "owens",
        #     "email": "phillip@gmail.com",
        #     "password": "1234"
        # }
        data2 = {
            "business": "SMILE FOOD",
            "location": "Kawempe",
            "firstname": "friend",
            "lastname": "stuart",
            "email": "pfriend@gmail.com",
            "password": "1234"
        }
        # self.assertEqual(admin.add_admin(data1), "Successfully Added")
        # self.assertEqual(admin.add_admin(data2), "Successfully Added")
        self.assertEqual(admin.remove_admin(1), "Successfully Removed")
        self.assertEqual(admin.get_admin(1), "No Admin Found")

    def test_update_admin(self):
        admin = Admin()
        # data1 = {
        #     "business": "FAST MEALS",
        #     "location": "Ntinda",
        #     "firstname": "phillip",
        #     "lastname": "owens",
        #     "email": "phillip@gmail.com",
        #     "password": "1234"
        # }
        data2 = {
            "business": "HAPPY FOOD",
            "location": "Kawempe",
            "firstname": "friend",
            "lastname": "stuart",
            "email": "pfriend@gmail.com",
            "password": "1234"
        }
        # self.assertEqual(admin.add_admin(data1), "Successfully Added")
        self.assertEqual(admin.update_admin(2, data2)['business'], "HAPPY FOOD")
        self.assertEqual(admin.update_admin(2, data2)['email'], "pfriend@gmail.com")


if __name__ == '__main__':
    unittest.main()
