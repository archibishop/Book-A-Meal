import datetime
from .data import Data

transactions = [
    {
        'id': 1,
        'meal_name': "ricebeans",
        'price': 3000,
        'user_id': 1,
        'process_status': "pending",
        'created_at': 'Fri, 04 May 2018 00:10:06 GMT',
        'updated_at': 'Fri, 04 May 2018 00:10:06 GMT'
    },
    {
        'id': 2,
        'meal_name': "lasagna",
        'price': 10000,
        'user_id': 2,
        'process_status': "pending",
        'created_at': 'Fri, 04 May 2018 00:10:06 GMT',
        'updated_at': 'Fri, 04 May 2018 00:10:06 GMT'
    },
    {
        'id': 3,
        'meal_name': 'rolex',
        'price': 4000,
        'user_id': 1,
        'process_status': "pending",
        'created_at': 'Fri, 04 May 2018 00:10:06 GMT',
        'updated_at': 'Fri, 04 May 2018 00:10:06 GMT'
    }
]

class Order():
    def __init__(self, meal_name, price, user_id):
        # self.orders = transactions
        # self.counter = 0
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
        """
        order_add = data
        if len(self.orders) == 0:
            new_id = 1
        else:    
            new_id = self.orders[-1].get("id") + 1
        order_add['id'] = new_id
        order_add['created_at'] = datetime.datetime.now()
        order_add['updated_at'] = datetime.datetime.now()
        self.orders.append(order_add)
        return "Successfully Made Order"
        """

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
