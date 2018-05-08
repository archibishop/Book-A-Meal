
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
        self.menu.append(menu_item)
        return menu_item

    def get_meal_menu(self, value):
        """ Getting onemeal from the menu """
        for menu_item in self.menu:
            if menu_item[id] == value:
                return menu_item
        return "Meal Not Found on Menu"        

    def get_full_menu(self):
        """ Getting Full Menu """
        return self.menu    

    def delete_meal_menu(self, value):
        """ Delete Meal From Menu """
        menu_item = self.get_meal_menu(value)
        if menu_item == "MealNot Found on Menu":
            return "Meal Not Found On Menu"
        self.menu.remove(menu_item)
        return "Meal Successfully Removed from the Menu"    

    def update__meal_menu(self, value, data):
        """ Update Meal In The Menu """
        menu_item = self.get_meal_menu(value)
        menu_item['updated_at'] = datetime.datetime.now()
        menu_item = data
        return "Meal has been Updated in the menu" 
