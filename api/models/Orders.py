from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from validate_email import validate_email
import datetime
from api import db
from werkzeug.security import generate_password_hash, check_password_hash
from api.models.Meals import Meals

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meal_name = db.Column(db.String(50))
    price = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    process_status = db.Column(db.String(50))
    created_at = db.Column(db.DateTime(timezone=True),
                           default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True),
                           onupdate=datetime.datetime.utcnow)

    def __init__(self, meal_name, price, user_id, process_status):
        self.meal_name = meal_name
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
        message, validation = '', True
        if not self.meal_name or not self.price or\
                not self.user_id:
            message, validation = "Some values missing in json data sent", False
        elif self.meal_name.strip() == '' or self.meal_name.strip() == '':
            message, validation = "You sent some empty strings", False
        elif len(self.meal_name) > 30:
            message, validation = "Meal name is too long", False
        elif len(self.meal_name) < 3:
            message, validation = "Meal name is too short", False
        elif not isinstance(self.price, int) or not isinstance(self.user_id, int):
            message, validation = "Price should be an integer", False
        elif Meals.get_meal_by_name(self.meal_name) == None:
            message, validation = "Meal Does Not Exist", False
        if not validation:
            return message    
        return "Valid Data Sent"

    @staticmethod
    def validate_json(data):
        message, validation = '', True
        if data is None:
            message, validation =  "No JSON DATA sent", False
        if 'meal_name' not in data or 'price' not in data:
            message, validation = "Some values missing in json data sent", False
        if type(data.get('price')) is not int:
            message, validation = "Price should be Integer", False
        if data.get('meal_name') == '':
            message, validation = "Meal Name is Empty", False
        if not validation:
            return message    
        return "Valid Data Sent"
