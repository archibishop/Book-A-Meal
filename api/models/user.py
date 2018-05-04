import datetime

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
    def __init__(self):
        self.users = users
        self.counter = 0

    def add_user(self, data):
        user_add = data
        email = user_add['email']

        for user in self.users:
            if user["email"] == email:
                return "Email Exists" 
        if len(self.users) == 0:
            new_id = 1
        else:    
            new_id = self.users[-1].get("id") + 1
        user_add['id'] = new_id
        user_add['created_at'] = datetime.datetime.now()
        user_add['updated_at'] = datetime.datetime.now()
        self.users.append(user_add)
        return user_add

    def get_user(self, value):
        for user in self.users:
            if user['id'] == value:
                return user
        return "No User Found"

    """ We need to add test for this """
    def check_user_email_password(self, email, password):
        for user in self.users:
            if user['email'] == email:
                if user['password'] == password:
                    return True
                else:
                    return "Wrong Password or UserName"           
        return "No User Found With That Email"    

    def get_all_users(self):
        return self.users

    def remove_user(self, value):
        for user in self.users:
            if user['id'] == value:
                self.users.remove(user)
                return "Successfully Removed"
        return "No User Found"

    def update_user(self, value, data):
        user = self.get_user(value)
        user['updated_at'] = datetime.datetime.now()
        user = data
        return user
