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
