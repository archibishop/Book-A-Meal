from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
import datetime
from api import db

"""
Change to persistent data, using sql alchemy 
"""

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))
    role_id = db.Column(db.Integer)
    business_name = db.Column(db.String(50))
    location = db.Column(db.String(50))
    created_at = db.Column(db.DateTime(timezone=True),\
    default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True),\
    onupdate=datetime.datetime.utcnow)
    meal = db.relationship('Orders', backref='user', lazy=True) 
    menu = db.relationship('Menu', backref='user', lazy=True)

    def __init__(self, first_name, last_name, email, password, business_name, location, role_id):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email 
        self.password = password 
        self.business_name =  business_name
        self.location = location
        self.role_id = role_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()    

    @staticmethod
    def get_user_email(email):
        user = User.query.filter_by(email=email).first()
        if not user:
            return "No User"
        return user

    @staticmethod
    def validate_json(data):
        if data is None:
            return "No JSON DATA sent"
        if 'fname' not in data or 'lname' not in data or 'email' not in data\
                or 'password' not in data or 'role_id' not in data:
            return "Some values missing in json data sent"
        if data.get('fname') == '' or data.get('lname') == '' or data.get('email') == ''\
                or data.get('password') == '':
            return "You sent some empty strings"
        if type(data.get('role_id')) is not int:
            return "Role id should be an integer"   
        if len(data.get('password')) < 5:
            return "Password provided is too short.A minimum of 5 characters required"
        return "Valid Data Sent"

    
    @staticmethod
    def validate_json_1(data):  
        if 'business_name' not in data or 'location' not in data:
            return "Some values missing in json data sent"
        if data.get('business_name') == '' or data.get('location') == '':
            return "You sent some empty strings"  
        return "Valid Data Sent" 

    @staticmethod
    def validate_json_login(data):
        if data is None:
            return "No Data Sent"
        if 'email' not in data or 'password' not in data:
            return "Some values missing in json data sent"
        if data.get('email') == '' or data.get('password') == '':
            return "You sent some empty strings"
        return "Valid Data Sent"
  

class Meals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meal_name = db.Column(db.String(50), unique=True)
    price = db.Column(db.Integer)
    meal_type = db.Column(db.String(50))
    created_at = db.Column(db.DateTime(timezone=True),\
    default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True),\
    onupdate=datetime.datetime.utcnow)   

    def __init__(self, meal_name, price, meal_type):
        self.meal_name = meal_name
        self.price = price
        self.meal_type = meal_type

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete_meal(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_meals():
        return Meals.query.all()

    @staticmethod
    def get_meal_by_name(meal_name):
        meal = Meals.query.filter_by(meal_name=meal_name).first()
        return meal

    @staticmethod
    def get_meal_by_id(id):
        meal = Meals.query.filter_by(id=id).first()  
        return meal

    @staticmethod
    def update_meal(id, meal_name, price, meal_type): 
        meal = Meals.get_meal_by_id(id)
        if not meal:
            return "Meal Does Not Exist"
        if meal.meal_name != meal_name:
            meal.meal_name = meal_name

        meal.price = price
        meal.meal_type = meal_type
        db.session.commit()
        return meal

    @staticmethod
    def validate_json(data):
        if data is None:
            return "No JSON DATA sent"
        if 'meal_name' not in data or 'price' not in data or\
            'meal_type' not in data:
            return "Some values missing in json data sent"
        if data.get('meal_name') == '' or data.get('meal_type') == '':
            return "You sent some empty strings"
        if type(data.get('price')) is not int:
            return "Price should be an integer"
        return "Valid Data Sent"

    @staticmethod
    def validate_json_1(data):
        if data is None:
            return "No JSON DATA sent"
        if 'meal_name' not in data or 'price' not in data or\
                'user_id' not in data:
            return "Some values missing in json data sent"
        if data.get('meal_name') == '':
            return "You sent some empty strings"
        if type(data.get('price')) is not int or type(data.get('user_id')) is not int:
            return "Price or User id should be an integer"
        return "Valid Data Sent"


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meal_name = db.Column(db.String(50))
    price = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    process_status = db.Column(db.String(50))
    created_at = db.Column(db.DateTime(timezone=True),\
    default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True),\
    onupdate=datetime.datetime.utcnow)

    def __init__(self, meal_name, price, user_id, process_status):
        self.meal_name =  meal_name
        self.price = price
        self.user_id = user_id
        self.process_Status = process_status

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete_order(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_orders():
        return Orders.query.all()  

    @staticmethod
    def get_order_by_id(id):
        order = Orders.query.filter_by(id=id).first()  
        return order 

    @staticmethod
    def update_order(id, meal_name, price):
        order = Orders.get_order_by_id(id) 
        if not order:
            return "Order does not exist"

        #Since mealName should be unqiue in the database Updating the same name causes Integrity Error
        if order.meal_name != meal_name:
            order.meal_name = meal_name

        order.price = price
        db.session.commit()
        return order

    @staticmethod
    def validate_json(data):
        if data is None:
            return "No JSON DATA sent"
        if 'meal_name' not in data or 'price' not in data:
            return "Some values missing in json data sent"
        if type(data.get('price')) is not int:
            return "Price should be Integer"
        if data.get('meal_name') == '':
            return "Meal Name is Empty"
        return "Valid Data Sent"
    
        

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    meal_ids = db.Column(db.String(50))
    created_at = db.Column(db.DateTime(timezone=True),\
    default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True),\
    onupdate=datetime.datetime.utcnow)

    def __init__(self, user_id, meal_ids):
        self.user_id = user_id
        self.meal_ids = meal_ids

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete_menu(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_menus():
        return Menu.query.all() 

    @staticmethod
    def get_menu_by_id(id):
        menu = Menu.query.filter_by(id=id).first()
        return menu

    @staticmethod
    def get_menu_by_user_id(user_id):
        menu = Menu.query.filter_by(user_id=user_id).first()
        return menu  

    @staticmethod
    def update_menu(id, meal_ids):
        # menu = Menu.get_menu_by_id(id)
        menu = Menu.query.filter_by(id=id).first()
        if not menu:
            return "No Meal Found"

        meal_ids_string = ""
        for ids in meal_ids:
            if ids != "":
                meal_ids_string += ';%s' % ids

        menu.meal_ids = meal_ids_string
        db.session.commit()
        return menu

    @staticmethod
    def validate_json(data):
        if data is None:
            return "No JSON DATA sent"
        if 'meal_ids' not in data or 'user_id' not in data:
            return "Some values missing in json data sent"
        if type(data.get('user_id')) is not int:
            return "User Id should be Integer"
        if len(data.get('meal_ids')) == 0:
            return "Meal ids is Empty"
        return "Valid Data Sent"
