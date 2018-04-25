
class User():
    def __init__(self):
        self.users = []
        self.counter = 0

    def addUser(self, data):
        user = data
        self.counter =  self.counter + 1
        user['id'] = self.counter
        self.users.append(user)
        return "Successfully Added"

    def getUser(self, value):
        for user in self.users:
            if user['id'] == value:
                return user
        return "No User Found"

    def getAllUsers(self):
        return self.users    

    def removeUser(self, value):
        for user in self.users:
            if user['id'] == value:
                self.users.remove(user)
                return "Successfully Removed"
        return "No User Found"

    def updateUser(self, value, data):
        user = self.getUser(value)
        user = data 
        return user


