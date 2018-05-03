import datetime

transactions = [
    {
        'id': 1,
        'meal_name': "ricebeans",
        'price': 3000,
        'user_id': 1,
        'process_status': "pending"
    },
    {
        'id': 2,
        'meal_name': "lasagna",
        'price': 10000,
        'user_id': 2,
    },
    {
        'id': 3,
        'meal_name': 'rolex',
        'price': 4000,
        'user_id': 1,
    }
]

class Order():
    def __init__(self):
        self.orders = transactions
        self.counter = 0

    def place_order(self, data):
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

    def get_order(self, value):
        for order in self.orders:
            if order['id'] == value:
                return order
        return "No Order Found"

#test case for this
    def get_all_orders(self):
        return self.orders    

    def get_orders_user(self, value):
        ordersUser = []
        for order in self.orders:
            if order['user_id'] == value:
                ordersUser.append(order)
        if ordersUser != []:
            return ordersUser
        else:
            return ordersUser


    def remove_order(self, value):
        for order in self.orders:
            if order['id'] == value:
                self.orders.remove(order)
                return "Successfully Removed"
        return "No Order Found"

    def update_order(self, value, data):
        order = self.get_order(value)
        order['meal_name'] = data['meal_name']
        order['price'] = data['price']
        order['updated_at'] = datetime.datetime.now()
        return order
