from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from validate_email import validate_email
import datetime
from api import db
from werkzeug.security import generate_password_hash, check_password_hash

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
    
    def validate(self):
        if not self.first_name or not self.last_name\
                or not self.email or not self.password:
            return "Missing Values in Json Data sent"
        if not self.first_name.strip() or  not self.last_name.strip()\
                or not self.email.strip() or not self.password.strip()\
                or not isinstance(self.role_id, int):  
            return "Empty values missing in json data sent"
        if self.role_id == 1:
            if not self.business_name.strip() or not self.location.strip():
                return "Some values missing in json data sent"
            elif len(self.business_name) < 3 or len(self.location) < 3:
                return "Business name or location too short"
        else:
            self.business_name = ""
            self.location = ""
        if len(self.first_name) < 3 or len(self.last_name) < 3 or\
            len(self.password) < 5:
            return "Password/Firstname/lastname provided is too short."
        is_valid = validate_email(self.email)
        if not is_valid:
            return "Wrong Email Format Sent"
        email_exists = User.query.filter_by(email=self.email).first()
        if email_exists != None:
            return 'Email Already Exists'
        hashed_password = generate_password_hash(self.password, method='sha256') 
        self.password = hashed_password
        return "Valid Data Sent"


    @staticmethod
    def validate_json_login(data):
        if data is None:
            return "No Data Sent"
        if 'email' not in data or 'password' not in data:
            return "Some values missing in json data sent"
        if data.get('email').strip() == '' or data.get('password').strip() == '':
            return "You sent some empty strings"
        user = User.get_user_email(data.get('email'))
        if user == "No User":
            return 'User Not Found'
        if not check_password_hash(user.password, data.get('password')):
            return "Wrong Password"
        return user
  

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
        meal = Meals(meal_name=meal_name, price=price, meal_type=meal_type)
        message = meal.validate_json()
        if message != "Valid Data Sent":
            return message
        meal = Meals.get_meal_by_id(id)
        if not meal:
            return "Meal Does Not Exist"   
        if meal.meal_name != meal_name:
            meal.meal_name = meal_name
        meal.price = price
        meal.meal_type = meal_type
        db.session.commit()
        return meal

    def validate_json(self):
        if not self.meal_name or not self.price or\
                not self.meal_type:   
            return "Some values missing in json data sent"
        if self.meal_name.strip() == '' or self.meal_type.strip() == '':
            return "You sent some empty strings"
        if not isinstance(self.price, int):
            return "Price should be an integer"
        meal_exists = Meals.get_meal_by_name(self.meal_name)
        if meal_exists != None:
            return "Meal Already Exists"
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
        self.process_status = process_status

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

    def validate_json_object(self):
        if not self.meal_name or not self.price or\
                not self.user_id:
            return "Some values missing in json data sent"
        if self.meal_name.strip() == '' or self.meal_name.strip() == '':
            return "You sent some empty strings"
        if not isinstance(self.price, int) or not isinstance(self.user_id, int):
            return "Price should be an integer"
        meal_exists = Meals.get_meal_by_name(self.meal_name)
        if meal_exists == None:
            return "Meal Does Not Exist"
        return "Valid Data Sent"

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

    def validate_json_object(self):
        if not self.user_id or not self.meal_ids:
            return "Some values missing in json data sent"
        if not isinstance(self.user_id, int):
            return "User Id should be Integer"
        if not isinstance(self.meal_ids, str):
            return "Meal ids is Empty"
        caterer = Menu.get_menu_by_user_id(self.user_id)
        if caterer is not None:
            return 'Caterer Already Set Menu For the Day'
        return "Valid Data Sent"

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

    @staticmethod
    def convert_into_list(menu):
        converted_meal_ids = []
        for idx in menu.meal_ids.split(';'):
            if idx != "":
                converted_meal_ids.append(int(idx))
        return converted_meal_ids   

    @staticmethod
    def convert_into_string(meal_ids):
        meal_ids_string = ""
        for ids in meal_ids:
            meal_ids_string += ';%s' % ids 
        return meal_ids_string      
