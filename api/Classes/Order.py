import datetime


class Order():
    def __init__(self):
        self.orders = []
        self.counter = 0

    def place_order(self, data):
        order = data
        self.counter = self.counter + 1
        order['id'] = self.counter
        order['created_at'] = datetime.datetime.now()
        order['updated_at'] = datetime.datetime.now()
        self.orders.append(order)
        return "Successfully Made Order"

    def get_order(self, value):
        for order in self.orders:
            if order['id'] == value:
                return order
        return "No Order Found"

    def get_orders_user(self, value):
        ordersUser = []
        for order in self.orders:
            if order['customerId'] == value:
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
        order = data
        order['updated_at'] = datetime.datetime.now()
        return order
