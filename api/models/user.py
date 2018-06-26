import datetime
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
        for user in Data.users:
            if user.email == self.email:
                return "Email Exists"    
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


    @staticmethod
    def validate(data):
        if data is None:
            return "No JSON DATA sent"
        if 'fname' not in data or 'lname' not in data or 'email' not in data\
            or 'password' not in data:
            return "Some values missing in json data sent"
        if data.get('fname') == '' or data.get('lname') == '' or data.get('email') == ''\
                or data.get('password') == '':
            return "You sent some empty strings"  
        is_valid = validate_email(data.get('email'))
        if not is_valid:
            return "Wrong Email Format Sent"
        if len(data.get('password')) < 5:
            return "Password provided is too short.A minimum of 5 characters required"
        return "Valid Data Sent"

    @staticmethod
    def validate_login(data):
        if data is None:
            return "No JSON DATA sent"
        if 'email' not in data or 'password' not in data:
            return "Missing Values in Data Sent"
        if data.get('email') == '' or data.get('password') == '':
            return "You sent some empty strings"
        return "Valid Data Sent"    


