import datetime


class Admin():
    def __init__(self):
        self.admins = []
        self.counter = 0

    def add_admin(self, data):
        admin = data
        self.counter = self.counter + 1
        admin['id'] = self.counter
        admin['created_at'] = datetime.datetime.now()
        admin['updated_at'] = datetime.datetime.now()
        self.admins.append(admin)
        return "Successfully Added"

    def get_admin(self, value):
        for admin in self.admins:
            if admin['id'] == value:
                return admin
        return "No Admin Found"

    def remove_admin(self, value):
        for admin in self.admins:
            if admin['id'] == value:
                self.admins.remove(admin)
                return "Successfully Removed"
        return "No Admin Found"

    def update_admin(self, value, data):
        admin = self.get_admin(value)
        admin['updated_at'] = datetime.datetime.now()
        admin = data
        return admin
