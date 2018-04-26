import unittest

from Admin import Admin


class TestAdmin(unittest.TestCase):
    def test_add_admin(self):
        admin = Admin()
        data = {
            "business": "FAST MEALS",
            "location": "Ntinda",
            "firstname": "phillip",
            "lastname": "owens",
            "email": "phillip@gmail.com",
            "password": "1234"
        }
        self.assertEqual(admin.addAdmin(data), "Successfully Added")

    def test_get_admin(self):
        admin = Admin()
        data1 = {
            "business": "FAST MEALS",
            "location": "Ntinda",
            "firstname": "phillip",
            "lastname": "owens",
            "email": "phillip@gmail.com",
            "password": "1234"
        }
        data2 = {
            "business": "HAPPY FOOD",
            "location": "Kawempe",
            "firstname": "friend",
            "lastname": "stuart",
            "email": "pfriend@gmail.com",
            "password": "1234"
        }

        self.assertEqual(admin.addAdmin(data1), "Successfully Added")
        self.assertEqual(admin.addAdmin(data2), "Successfully Added")
        self.assertEqual(admin.getAdmin(2), data2)
        self.assertEqual(admin.getAdmin(1), data1)
        self.assertEqual(admin.getAdmin(3), "No Admin Found")

    def test_remove_admin(self):
        admin = Admin()
        data1 = {
            "business": "FAST MEALS",
            "location": "Ntinda",
            "firstname": "phillip",
            "lastname": "owens",
            "email": "phillip@gmail.com",
            "password": "1234"
        }
        data2 = {
            "business": "HAPPY FOOD",
            "location": "Kawempe",
            "firstname": "friend",
            "lastname": "stuart",
            "email": "pfriend@gmail.com",
            "password": "1234"
        }
        self.assertEqual(admin.addAdmin(data1), "Successfully Added")
        self.assertEqual(admin.addAdmin(data2), "Successfully Added")
        self.assertEqual(admin.removeAdmin(1), "Successfully Removed")
        self.assertEqual(admin.getAdmin(1), "No Admin Found")
        self.assertEqual(admin.getAdmin(2), data2)

    def test_update_admin(self):
        admin = Admin()
        data1 = {
            "business": "FAST MEALS",
            "location": "Ntinda",
            "firstname": "phillip",
            "lastname": "owens",
            "email": "phillip@gmail.com",
            "password": "1234"
        }
        data2 = {
            "business": "HAPPY FOOD",
            "location": "Kawempe",
            "firstname": "friend",
            "lastname": "stuart",
            "email": "pfriend@gmail.com",
            "password": "1234"
        }
        self.assertEqual(admin.addAdmin(data1), "Successfully Added")
        self.assertEqual(admin.updateAdmin(1, data2), data2)


if __name__ == '__main__':
    unittest.main()
