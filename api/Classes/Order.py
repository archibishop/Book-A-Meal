import datetime

class Order():
    def __init__(self):
        self.orders = []
        self.counter = 0

    def placeOrder(self, data):
        order = data
        self.counter =  self.counter + 1
        order['id'] = self.counter
        order['created_at'] = datetime.datetime.now()
        order['updated_at'] = datetime.datetime.now()
        self.orders.append(order)
        return "Successfully Made Order"

    def getOrder(self, value):
        for order in self.orders:
            if order['id'] == value:
                return order
        return "No Order Found"   

    def removeOrder(self, value):
        for order in self.orders:
            if order['id'] == value:
                self.orders.remove(order)
                return "Successfully Removed"
        return "No Order Found"

    def updateOrder(self, value, data):
        order = self.getOrder(value)
        order = data
        order['updated_at'] = datetime.datetime.now() 
        return order