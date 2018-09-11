from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
import datetime
from api import db

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meal_name = db.Column(db.String(50), unique=True)
    price = db.Column(db.Integer)
    meal_type = db.Column(db.String(50))
    created_at = db.Column(db.DateTime(timezone=True),
                           default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True),
                           onupdate=datetime.datetime.utcnow)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def __init__(self, meal_name, price, meal_type, admin_id):
        # meal model constructor.
        self.meal_name = meal_name
        self.price = price
        self.meal_type = meal_type
        self.admin_id = admin_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete_meal(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_meals():
        return Meal.query.all()

    @staticmethod
    def get_meals_by_admin_id(id):
        meals = Meal.query.filter_by(admin_id=id)
        return meals

    @staticmethod
    def get_meal_by_name(meal_name):
        meal = Meal.query.filter_by(meal_name=meal_name).first()
        return meal

    @staticmethod
    def get_meal_by_id(id):
        meal = Meal.query.filter_by(id=id).first()
        return meal

    @staticmethod
    def update_meal(id, meal_name, price, meal_type, admin_id):
        meal = Meal(meal_name=meal_name, price=price, meal_type=meal_type, admin_id=admin_id)
        message = meal.validate_json()
        if message != "Valid Data Sent":
            return message
        meal = Meal.get_meal_by_id(id)
        if not meal:
            return "Meal Does Not Exist"
        if meal.meal_name != meal_name:
            meal.meal_name = meal_name
        meal.price = price
        meal.meal_type = meal_type
        db.session.commit()
        return meal

    def validate_json(self):
        message, validation = '', True
        if not self.meal_name or not self.price or\
                not self.meal_type:
            message, validation = "Some values missing in json data sent", False
        elif self.meal_name.strip() == '' or self.meal_type.strip() == '':
            message, validation = "You sent some empty strings", False
        elif not isinstance(self.price, int) or not isinstance(self.admin_id, int):
            message, validation = "Price should be an integer", False
        elif len(self.meal_type) < 3 or len(self.meal_name) < 3:
            message, validation = "Meal name/type is too short", False
        elif len(self.meal_type) > 30 or len(self.meal_name) > 30:
            message, validation = "Meal name/type is too short", False
        elif Meal.get_meal_by_name(self.meal_name) != None:
            message, validation = "Meal Already Exists", False
        if not validation:
            return message    
        return "Valid Data Sent"


        
