from flask import Flask, jsonify, request, abort, session, Blueprint, current_app
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import datetime
import jwt
from api import db
from .models.models import User, Menu, Order, Meal
from .utils import is_admin, token_required

api_route = Blueprint("api", __name__)


@api_route.route('/bookmealapi/v1.0/menu', methods=['POST'])
@is_admin
@token_required
def set_menu():
    """ file: apidocs/set_menu.yml """
    data = request.get_json()
    meal_ids_string = Menu.convert_into_string(data.get('meal_ids'))
    menu = Menu(user_id=data.get('user_id'),
                meal_ids=meal_ids_string, menu_date=data.get('menu_date'))
    message = menu.validate_json_object()
    if message != "Valid Data Sent":
        return jsonify({'message': message}), 400
    menu.save()
    menu_info = {}
    menu_info['id'] = menu.id
    menu_info['user_id'] = menu.user_id
    # Converting the meal ids into a list again 
    converted_meal_ids = Menu.convert_into_list(menu)
    menu_info['meal_ids'] = converted_meal_ids
    menu_info['created_at'] = menu.created_at
    menu_info['updated_at'] = menu.updated_at
    menu_info['menu_date'] = menu.menu_date
    return jsonify({'message':'Menu Successfully Created',\
      'menu': menu_info}), 201              
       

@api_route.route('/bookmealapi/v1.0/orders/<order_id>', methods=['PUT'])
@token_required
def update_order(order_id):
    """ file: apidocs/update_order.yml """   
    data = request.get_json()
    message = Order.validate_json(data)
    if message != "Valid Data Sent":
        return jsonify({'message': message}), 400
    meal_name = data.get('meal_name')    
    response = Order.update_order(order_id, meal_name)
    if response == "Order does not exist":
        return jsonify({'message': 'Order Does Not Exist'}), 404
    output = {}
    output['id'] = response.id
    output['meal_name'] = response.meal_name
    output['price'] = response.price
    output['user_id'] = response.user_id
    output['created_at'] = response.created_at
    output['updated_at'] = response.updated_at
    return jsonify({'message': 'Order Updated', 'order': output}), 201    

@api_route.route('/bookmealapi/v1.0/menu/<menu_id>', methods=['PUT'])
@is_admin
@token_required
def update_menu(menu_id):
    """ file: apidocs/update_menu.yml """       
    data = request.get_json()
    message = Menu.validate_json(data)
    if message != "Valid Data Sent":
        return jsonify({'message': message}), 400
    response = Menu.update_menu(menu_id, data.get('meal_ids'))
    if response == "No Meal Found":
        return jsonify({'message': 'Menu Does Not Exist'}), 404
    menu_info = {}
    menu_info['id'] = response.id
    menu_info['user_id'] = response.user_id
    # Converting the meal ids into a list again 
    converted_meal_ids = Menu.convert_into_list(response)
    menu_info['meal_ids'] = converted_meal_ids
    menu_info['created_at'] = response.created_at
    menu_info['updated_at'] = response.updated_at
    return jsonify({'message': "Meal has been Updated in the menu",\
          'menu': menu_info}), 201               


@api_route.route('/bookmealapi/v1.0/menu', methods=['GET'])
@token_required
def get_menu():
    """ file: apidocs/get_menu.yml """
    menus = Menu.get_all_menus()
    output = []
    for menu in menus:
        menu_info = {}
        menu_info['id'] = menu.id
        menu_info['user_id'] = menu.user_id
        # Converting the meal ids into a list again 
        converted_meal_ids = Menu.convert_into_list(menu)
        menu_info['meal_ids'] = converted_meal_ids
        menu_info['created_at'] = menu.created_at
        menu_info['updated_at'] = menu.updated_at
        output.append(menu_info)
    return jsonify({'menu_day': output}), 200


@api_route.route("/bookmealapi/v1.0/menu/<menu_id>", methods=['DELETE'])
@token_required
def delete_menu(menu_id):
    """ file: apidocs/delete_menu.yml """
    """ Delete menu """
    menu = Menu.get_menu_by_id(menu_id)
    if not menu:
        return jsonify({'message':'Menu Does Not Exist'}), 404
    menu.delete_menu()
    return jsonify({'message':'Menu Successfully removed'}), 200


@api_route.route("/bookmealapi/v1.0/caterers", methods=['GET'])  
@token_required  
def get_caterers():
    """ Get Caterers """
    caterers = User.get_caterers()
    output = []
    for user in caterers:
        user_info = {}
        user_info['id'] = user.id
        user_info['business_name'] = user.business_name
        output.append(user_info)
    return jsonify({'Caterers': output}), 200

@api_route.route("/bookamealapi/v1.0/caterers/<caterer_id>", methods=['GET'])
@token_required
def get_caterers_menu(caterer_id):
    """ Get caterers menu"""
    meals = Menu.get_menu_by_user_id(caterer_id)
    output = output = get_menu_list(meals)
    return jsonify({'Menu': output}), 200
    # return jsonify({'Menu': output}), 404


@api_route.route("/bookamealapi/v1.0/days_of_week", methods=['GET'])
def get_days():
    """ Get days of week"""
    date_list = []
    date_count = datetime.date.today().weekday()
    for count in range(0, 7):        
        if count >= date_count:
            diff = (6 - count) + date_count
            date = datetime.date.today() + datetime.timedelta(6-count)
            day = date.strftime("%A")
            day_data = {
                "val": diff,
                "day": day
            }
            date_list.append(day_data)
    return jsonify({'days': date_list}), 200
    

@api_route.route("/bookamealapi/v1.0/menu/day/<day_val>", methods=['POST'])
@token_required
def get_menu_day(day_val):
    """ Get menu by day"""
    data = request.get_json()
    meals, date_list, menu_id = Menu.get_menu_by_day(int(day_val), data.get('value'))
    output = get_menu_list(meals)
    return jsonify({'menu_day': output, 'date_list': date_list, 'menu_id': menu_id}), 200


@api_route.route("/bookamealapi/v1.0/menu/days/<caterer_id>", methods=['GET'])
@token_required
def get_menu_days(caterer_id):
    """ Get menu by day"""
    days = Menu.get_menu_days(caterer_id)
    return jsonify({'days_list': days}), 200
    

def get_menu_list(meals):
    output = []
    if len(meals) > 0:
        for meal in meals:
            item_info = {}
            item_info['id'] = meal.id
            item_info['meal_name'] = meal.meal_name
            item_info['meal_type'] = meal.meal_type
            item_info['price'] = meal.price
            item_info['admin_id'] = meal.admin_id
            output.append(item_info)
    return output        
