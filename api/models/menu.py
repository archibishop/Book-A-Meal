
import datetime
from .data import Data

class Menu():
    """ Menu Class """
    def __init__(self, meal_ids, user_id):
        self.meal_ids = meal_ids
        self.user_id = user_id
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        if len(Data.menu) > 0:
            id = Data.menu[-1].id + 1
        else:
            id = 1
        self.id = id

    def add_meals_menu(self):
        """ Menu Class """
        Data.menu.append(self)
        return self
        

    @staticmethod
    def get_meal_menu(value):
        """ Getting onemeal from the menu """
        for menu_item in Data.menu:
            if menu_item.id == value:
                return menu_item
        return "Menu Not Found"        

    @staticmethod
    def get_full_menu():
        """ Getting Full Menu """
        output = []
        for menu in Data.menu:
            if menu.created_at.date() == datetime.datetime.today().date():
                output.append(menu)
        return output

    @staticmethod
    def remove_meal_menu(value):
        """ Delete Meal From Menu """
        menu_item = Menu.get_meal_menu(value)
        if menu_item == "Menu Not Found":
            return "Menu Not Found"
        Data.menu.remove(menu_item)
        return "Menu Successfully removed"    

    @staticmethod
    def update_meal_menu(value, data):
        """ Update Meal In The Menu """
        menu_item = Menu.get_meal_menu(value)
        menu_item.updated_at = datetime.datetime.now()
        menu_item.meal_ids = data['meal_ids']
        menu_item.user_id = data['user_id']
        return menu_item 

    def validate(self):
        message, validation = '', True
        if self.meal_ids is None or self.user_id is None:
            message, validation = "Missing Values in Data Sent", False
        elif  len(self.meal_ids) ==  0:
            message, validation = "You sent some empty strings", False
        elif not isinstance(self.user_id, int):
            message, validation = "User Id should be Integer", False
        if not validation:
            return message    
        return "Valid Data Sent"

    @staticmethod
    def validate_json(data):
        message, validation = '', True
        if data is None:
            message, validation = "No Data Sent", False
        elif 'meal_ids' not in data or 'user_id' not in data:
            message, validation = "Missing Values in Data Sent", False   
        elif data.get('meal_ids') == '' or data.get('user_id') == '':
            message, validation = "You sent some empty strings", False
        elif type(data.get('user_id')) is not int:
            message, validation = "User Id should be Integer", False
        if not validation:
            return message    
        return "Valid Data Sent"    
