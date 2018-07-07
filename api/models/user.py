import datetime
from .admin import Admin
from .data import Data
from validate_email import validate_email


class User():
    id = 1
    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name 
        self.last_name = last_name
        self.email = email
        self.password = password
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        id = len(Data.users) + 1
        if len(Data.users) > 0:
            id = Data.users[-1].id + 1
        else:
            id  = 1
        
        self.id = id


    def add_user(self):    
        Data.users.append(self)
        return self


    @staticmethod
    def get_user(value):
        for user in Data.users:
            if user.id == value:
                return user
        return "No User Found"   

    """ We need to add test for this """
    @staticmethod
    def check_user_email_password(email, password):
        for user in Data.users:
            if user.email == email:
                if user.password == password:
                    return True
                else:
                    return "Wrong Password or UserName"           
        return "No User Found With That Email"  

    @staticmethod
    def get_all_users():
        return Data.users
 
    @staticmethod
    def remove_user(value):
        for user in Data.users:
            if user['id'] == value:
                Data.users.remove(user)
                return "Successfully Removed"
        return "No User Found"

    @staticmethod
    def update_user(value, data):
        for user in Data.users:
            if user['id'] == value:
                user['updated_at'] = datetime.datetime.now()
                user = data
        return user

    def validate_json(self):
        if self.first_name is None or self.last_name is None or self.email is None\
            or self.password is None:
            return "Some values missing in json data sent"
        if self.first_name.strip() == '' or self.last_name.strip() == '' or\
                self.email.strip() == '' or self.password.strip() == '':
            return "You sent some empty strings"
        is_valid = validate_email(self.email)
        if not is_valid:
            return "Wrong Email Format Sent"
        if len(self.password) < 5:
            return "Password provided is too short.A minimum of 5 characters required"
        for user in Data.users:
            if user.email == self.email:
                return "Email Already Exists"
        return "Valid Data Sent"

    @staticmethod
    def validate_login(data):
        if data is None:
            return "No JSON DATA sent"
        if 'email' not in data or 'password' not in data:
            return "Missing Values in Data Sent"
        if data.get('email').strip() == '' or data.get('password').strip() == '':
            return "You sent some empty strings"
        if User.check_user_email_password(
            data.get('email'), data.get('password')) is True:
            return "User"
        if Admin.check_admin_email_password(
            data.get('email'), data.get('password')) is True:
            return "Admin"
        return "User Not Found"


