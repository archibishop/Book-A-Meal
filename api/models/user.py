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
    def user_exists(email):
        for user in Data.users:
            if user.email == email:
                return True
        return False

    @staticmethod
    def update_user(value, data):
        for user in Data.users:
            if user['id'] == value:
                user['updated_at'] = datetime.datetime.now()
                user = data
        return user

    def validate_json(self):
        message, validation = '', True
        if self.first_name is None or self.last_name is None or self.email is None\
            or self.password is None:
            message, validation = "Some values missing in json data sent", False
        elif self.first_name.strip() == '' or self.last_name.strip() == '' or\
                self.email.strip() == '' or self.password.strip() == '':
            message, validation = "You sent some empty strings", False
        elif not validate_email(self.email):
            message, validation = "Wrong Email Format Sent", False
        elif len(self.password) < 5:
            message, validation = "Password provided is too short.A minimum of 5 characters required", False
        elif self.user_exists(self.email):
            message, validation = "Email Already Exists", False
        if not validation:
            return message
        return "Valid Data Sent"

    @staticmethod
    def validate_login(data):
        message, validation = '', True
        if data is None:
            message, validation = "No JSON DATA sent", False
        elif 'email' not in data or 'password' not in data:
            message, validation = "Missing Values in Data Sent", False
        elif data.get('email').strip() == '' or data.get('password').strip() == '':
            message, validation = "You sent some empty strings", False
        elif User.check_user_email_password(
            data.get('email'), data.get('password')) is True:
            message, validation = "User", False
        elif Admin.check_admin_email_password(
            data.get('email'), data.get('password')) is True:
            message, validation = "Admin", False
        if not validation:
            return message
        return "User Not Found"


