import datetime
from .data import Data

users = [
    {
        'id': 1,
        'first_name': 'dennis',
        'last_name': 'lubega',
        'email': 'lubega@gmail.com',
        'password': '12345',
    },
    {
        'id': 2,
        'first_name': 'atlas',
        'last_name': 'Tegz',
        'email': 'atlas@gmail.com',
        'password': '12345',
    }
]


class User():
    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name 
        self.last_name = last_name
        self.email = email
        self.password = password
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        id = len(Data.users) + 1
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
            print(password)
            print(email)
            print(len(Data.users))
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
