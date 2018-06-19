
import datetime
from .data import Data

class Menu():
    """ Menu Class """
    def __init__(self, meal_ids, user_id):
        self.meal_ids = meal_ids
        self.user_id = user_id
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        id = len(Data.menu) + 1
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
