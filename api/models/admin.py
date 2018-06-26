import datetime
from .data import Data
from validate_email import validate_email


class Admin():
    def __init__(self, business_name, first_name, last_name, email, password):
        self.business_name = business_name
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password =password
        id = len(Data.admin) + 1 
        self.id = id

    def add_admin(self):
        for admin in Data.admin:
            if admin.email == self.email:
                return "Admin Already Exist"
        Data.admin.append(self)
        return "Successfully Added"

    
    @staticmethod
    def get_admin(value):
        for admin in Data.admin:
            if admin['id'] == value:
                return admin
        return "No Admin Found"

    """ add email test class """
    @staticmethod
    def check_admin_email_password(email, password):
        for admin in Data.admin:
            if admin.email == email:
                if admin.password == password:
                    return True
                else:
                    return "Wrong Password or UserName"           
        return "No User Found With That Email"    
 
    @staticmethod
    def remove_admin(value):
        for admin in Data.admin:
            if admin['id'] == value:
                Data.admin.remove(admin)
                return "Successfully Removed"
        return "No Admin Found"

    def update_admin(self, value, data):
        admin = self.get_admin(value)
        data2 = {
            "business": "HAPPY FOOD",
            "location": "Kawempe",
            "firstname": "friend",
            "lastname": "stuart",
            "email": "pfriend@gmail.com",
            "password": "1234"
        }
        admin['updated_at'] = datetime.datetime.now()
        admin['business'] = data['business']
        admin['location'] = data['location']
        admin['firstname'] = data['firstname']
        admin['lastname'] = data['lastname']
        admin['email'] = data['email']
        admin['password'] = data['password']
        return admin

    @staticmethod
    def validate(data):
        if data is None:
            return "No JSON DATA sent"
        if 'fname' not in data or 'lname' not in data or 'email' not in data\
                or 'password' not in data or 'business_name' not in data or \
                'locaton' not in data:
            return "Some values missing in json data sent"
        is_valid = validate_email(data.get('email'))
        if not is_valid:
            return "Wrong Email Format Sent"
        if data.get('fname') == '' or data.get('lname') == '' or \
                data.get('email') == '' or data.get('password') == '' or \
                data.get('business_name') == '' or data.get('location') == '':
            return "You sent some empty strings"
        if len(data.get('password')) < 5:
            return "Password provided is too short.A minimum of 5 characters required"    
        return "Valid Data Sent"
