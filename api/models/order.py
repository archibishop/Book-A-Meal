import datetime
from .data import Data

class Order():
    def __init__(self, meal_name, price, user_id):
        self.meal_name = meal_name
        self.price = price
        self.user_id = user_id
        self.process_status = "pending"
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        id = len(Data.orders) + 1
        self.id = id

    def place_order(self):
        Data.orders.append(self)
        return "Successfully Made Order"

    @staticmethod
    def get_order(value):
        for order in Data.orders:
            if order.id == value:
                return order
        return "No Order Found"

    """ test case for this """
    @staticmethod
    def get_all_orders():
        return Data.orders    

    @staticmethod
    def get_orders_user(value):
        ordersUser = []
        for order in Data.orders:
            if order.user_id == value:
                ordersUser.append(order)
        if ordersUser != []:
            return ordersUser
        else:
            return ordersUser


    @staticmethod
    def remove_order(value):
        for order in Data.orders:
            if order.id == value:
                Data.orders.remove(order)
                return "Successfully Removed"
        return "No Order Found"

    @staticmethod
    def update_order( value, data):
        order = Order.get_order(value)
        order.meal_name = data['meal_name']
        order.price = data['price']
        order.updated_at = datetime.datetime.now()
        return order
  
    def validate(self):
        if self.meal_name is None or self.price is None or \
                self.user_id is None:
            return "Missing Values"
        if self.meal_name.strip() == '':
            return "You sent some empty strings"
        if not isinstance((self.price), int) or not isinstance((self.user_id), int):
            return "Price Must Be Integer"
        return "Valid Data Sent"   

    @staticmethod
    def validate_json_1(data):
        if data is None:
            return "No Data Sent"
        if 'meal_name' not in data or 'price' not in data:
            return "Missing Values"
        if data.get('meal_name') == '' or data.get('price') == '':
            return "You sent some empty strings"    
        if not isinstance((data.get('price')), int):
            return "Price Must Be Integer"
        return "Valid Data Sent"

