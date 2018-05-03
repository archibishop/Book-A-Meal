import datetime

admin = [{
    'id': 1,
    'business_name': 'HAPPY FOODS',
    'location': 'NAKULABYE',
    'first_name': 'steven',
    'last_name': 'walube',
    'email': 'steven@gmail.com',
    'password': '54321',
}]


class Admin():
    def __init__(self):
        self.admins = admin
        self.counter = 0

    def add_admin(self, data):
        admin = data
        if len(self.admins) == 0:
            new_id = 1
        else:    
            new_id = self.admins[-1].get("id") + 1
        admin['id'] = new_id
        admin['created_at'] = datetime.datetime.now()
        admin['updated_at'] = datetime.datetime.now()
        self.admins.append(admin)
        return "Successfully Added"

    def get_admin(self, value):
        for admin in self.admins:
            if admin['id'] == value:
                return admin
        return "No Admin Found"

#add email test class
    def check_admin_email_password(self, email, password):
        for admin in self.admins:
            if admin['email'] == email:
                if admin['password'] == password:
                    return True
                else:
                    return "Wrong Password or UserName"           
        return "No User Found With That Email"    

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
