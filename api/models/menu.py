
import datetime



class Menu():
    """ Menu Class """
    def __init__(self):
        self.menu = []
        self.counter = 0

    def add_meals_menu(self, data):
        """ Menu Class """
        menu_item = data
        self.counter = self.counter + 1
        menu_item['id'] = self.counter
        menu_item['created_at'] = datetime.datetime.now()
        menu_item['updated_at'] = datetime.datetime.now()
        """ A caterer cannot have two mwnus"""
        self.menu.append(menu_item)
        return menu_item

    def get_meal_menu(self, value):
        """ Getting onemeal from the menu """
        for menu_item in self.menu:
            if menu_item['id'] == value:
                return menu_item
        return "Menu Not Found"        

    def get_full_menu(self):
        """ Getting Full Menu """
        return self.menu    

    def remove_meal_menu(self, value):
        """ Delete Meal From Menu """
        menu_item = self.get_meal_menu(value)
        if menu_item == "Menu Not Found":
            return "Menu Not Found"
        self.menu.remove(menu_item)
        return "Menu Successfully removed"    

    def update_meal_menu(self, value, data):
        """ Update Meal In The Menu """
        menu_item = self.get_meal_menu(value)
        menu_item['updated_at'] = datetime.datetime.now()
        menu_item['meal_ids'] = data['meal_ids']
        menu_item['user_id'] = data['user_id']
        return menu_item 
