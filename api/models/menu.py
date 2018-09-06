from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
import datetime
from datetime import timedelta, timezone
from api import db
from api.models.meal import Meal

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    meal_ids = db.Column(db.String(50))
    created_at = db.Column(db.DateTime(timezone=True),
                           default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True),
                           onupdate=datetime.datetime.utcnow)
    menu_date = db.Column(db.DateTime(timezone=True),
                           nullable=True)

    def __init__(self, user_id, meal_ids, menu_date):
        self.user_id = user_id
        self.meal_ids = meal_ids
        self.value = menu_date
        diff = (self.value - datetime.date.today().weekday())
        self.menu_date = datetime.date.today() + datetime.timedelta(diff)

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
    def get_menu_days(id):
        menus = Menu.query.filter_by(user_id=id).all()
        date_list = []
        dates = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        if menus:
            for menu in menus:
                date = menu.menu_date
                if date.date() >= datetime.datetime.now(timezone.utc).date():
                    day = date.strftime("%A")
                    if day in dates:
                        index = dates.index(day)
                        data = {
                            'id': menu.id,
                            'day': index
                        }
                    date_list.append(data) 

        return date_list


    @staticmethod
    def get_menu_by_day(val, user_id):
        diff = (val - datetime.date.today().weekday())
        date = datetime.date.today() + datetime.timedelta(diff)
        menu = Menu.query.filter_by(menu_date=date, user_id=user_id).first()
        output_meals = []
        menu_id = False
        if menu:
            if menu.menu_date.date() >= datetime.datetime.now(timezone.utc).date():
                if menu:
                    menu_id = menu.id
                    converted_meal_ids = Menu.convert_into_list(menu)
                    meals = Meal.get_all_meals()
                    for meal in meals:
                        if meal.id in converted_meal_ids:
                            output_meals.append(meal)
        date_list = Menu.get_menu_days(user_id)
        return output_meals, date_list, menu_id

    @staticmethod
    def get_menu_by_user_id(user_id):
        today = datetime.date.today()
        menu = Menu.query.filter_by(
            user_id=user_id, menu_date=datetime.date.today()).first()
        output_meals = []
        if menu:
            converted_meal_ids = Menu.convert_into_list(menu)
            meals = Meal.get_all_meals()
            for meal in meals:
                if meal.id in converted_meal_ids:
                    output_meals.append(meal)
        return output_meals

    @staticmethod
    def get_menu_by_user_id_exists(user_id):
        menu = Menu.query.filter_by(user_id=user_id).first()
        return menu
            
    @staticmethod
    def get_menu_by_day_exists(val, user_id):
        diff = (val - datetime.date.today().weekday())
        date = datetime.date.today() + datetime.timedelta(diff)
        menu = Menu.query.filter_by(menu_date=date, user_id=user_id).first()
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
        message, validation = '', True
        if not self.user_id or not self.meal_ids or not self.menu_date:
            message, validation = "Some values missing in json data sent", False
        elif not isinstance(self.user_id, int):
            message, validation = "User Id should be Integer", False
        elif not isinstance(self.meal_ids, str):
            message, validation = "Meal ids is Empty", False 
        elif Menu.get_menu_by_day_exists(self.value, self.user_id) is not None:
            value = Menu.get_menu_by_day_exists(self.value, self.user_id)
            message, validation = 'Caterer Already Set Menu For the Day', False
        if not validation:
            return message    
        return "Valid Data Sent"

    @staticmethod
    def validate_json(data):
        message, validation = '', True
        if data is None:
            message, validation = "No JSON DATA sent", False
        elif 'meal_ids' not in data or 'user_id' not in data:
            message, validation = "Some values missing in json data sent", False
        elif type(data.get('user_id')) is not int:
            message, validation = "User Id should be Integer", False
        elif len(data.get('meal_ids')) == 0:
            message, validation = "Meal ids is Empty", False
        elif len(data.get('meal_ids')) > 40:
            message, validation = "Meal ids is too long", False
        if not validation:
            return message    
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


        
