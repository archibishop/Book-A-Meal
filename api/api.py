from flask import Flask, jsonify, request, abort, session, Blueprint, current_app
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import datetime
import jwt
from api import db
from .models.models import User, Menu, Orders, Meals
from .utils import is_admin, token_required

api_route = Blueprint("api", __name__)

@api_route.route('/bookmealapi/v1.0/auth/signup', methods=['POST'])
def sign_up():
    """ file: apidocs/user_signup.yml """
    data = request.get_json()
    new_user = User(first_name=data.get('fname'), last_name=data.get('lname'),
                    email=data.get('email'), password=data.get('password'), 
                    role_id=data.get('role_id'), business_name=data.get('business_name'),
                    location=data.get('location'))
    response = new_user.validate()
    if response != "Valid Data Sent":
        return jsonify({'message': response}), 400     
    new_user.save()             
    return jsonify({'message' : 'New user created!'}), 201

@api_route.route('/bookmealapi/v1.0/auth/login', methods=['POST'])
def login():
    """ file: apidocs/user_login.yml  """    
    data =  request.get_json()
    response = User.validate_json_login(data)
    if response == "User Not Found":
        return jsonify({'message': response}), 404
    if response == "Wrong Password" or response == "Some values missing in json data sent":
        return jsonify({'message': response}), 400
    user = response    
    if user.role_id == 2:
        session['is_user'] = True
    else:
        session['admin'] = True
    token = jwt.encode({'id': user.id, 'exp': datetime.datetime.utcnow(
    ) + datetime.timedelta(minutes=30)}, current_app.config['SECRET_KEY'])
    return jsonify({'message':'Successfully login','token': token.decode('UTF-8')}), 200                 

@api_route.route('/bookmealapi/v1.0/meals', methods=['POST'])
@is_admin
@token_required
def add_meal():
    """ file: apidocs/add_meal.yml """   
    data = request.get_json()
    meal = Meals(meal_name=data.get('meal_name'), price=data.get('price'),\
                meal_type=data.get('meal_type'))
    response = meal.validate_json()
    if response != "Valid Data Sent":
        return jsonify({'message': response}), 400
    meal.save()
    return jsonify({'message' : 'Meal Successfully Added'}), 201      

@api_route.route('/bookmealapi/v1.0/orders', methods=['POST'])
@token_required
def select_meal():
    """ file: apidocs/select_meal.yml """    
    data = request.get_json()
    order = Orders(meal_name=data.get('meal_name'), price=data.get('price'),
     user_id=data.get('user_id'), process_status="pending")
    response = order.validate_json_object()
    if response != "Valid Data Sent":
        if response == "Meal Does Not Exist":
            return jsonify({'message', response}), 404
        else:    
            return jsonify({'message': response}), 400
    order.save()
    return jsonify({'message': "Transacrtion Successfully Made"}), 201

@api_route.route('/bookmealapi/v1.0/menu', methods=['POST'])
@is_admin
@token_required
def set_menu():
    """ file: apidocs/set_menu.yml """
    data = request.get_json()
    meal_ids_string = Menu.convert_into_string(data.get('meal_ids'))
    menu = Menu(user_id=data.get('user_id'), meal_ids=meal_ids_string)
    message = menu.validate_json_object()
    if message != "Valid Data Sent":
        return jsonify({'message', message}), 400
    menu.save()
    menu_info = {}
    menu_info['id'] = menu.id
    menu_info['user_id'] = menu.user_id
    # Converting the meal ids into a list again 
    converted_meal_ids = Menu.convert_into_list(menu)
    menu_info['meal_ids'] = converted_meal_ids
    menu_info['created_at'] = menu.created_at
    menu_info['updated_at'] = menu.updated_at
    return jsonify({'message':'Menu Successfully Created',\
      'menu': menu_info}), 201              

@api_route.route('/bookmealapi/v1.0/meals/<meal_id>', methods=['PUT'])
@is_admin
@token_required
def update_meal_option(meal_id):
    """ file: apidocs/update_meal.yml """
    data = request.get_json()
    response = Meals.update_meal(meal_id, data.get(
        'meal_name'), data.get('price'), data.get('meal_type'))
    if isinstance(response, str) and response != "Meal Does Not Exist":
        return jsonify({'message': "nothing"}), 400
    if response == "Meal Does Not Exist":
        return jsonify({'message':'Meal Does Not Exist'}),404    
    meal = response    
    meal_update = {}
    meal_update['id'] = meal.id
    meal_update['meal_name'] = meal.meal_name
    meal_update['price'] = meal.price
    meal_update['meal_type'] = meal.meal_type
    meal_update['created_at'] = meal.created_at
    meal_update['updated_at'] = meal.updated_at
    return jsonify({'message':'Meal Option Updated', 'meal':meal_update}), 201       

@api_route.route('/bookmealapi/v1.0/orders/<order_id>', methods=['PUT'])
@token_required
def update_order(order_id):
    """ file: apidocs/update_order.yml """   
    data = request.get_json()
    message = Orders.validate_json(data)
    if message != "Valid Data Sent":
        return jsonify({'message': message}), 400
    meal_name = data.get('meal_name')
    price = data.get('price')    
    response = Orders.update_order(order_id, meal_name, price)
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

@api_route.route('/bookmealapi/v1.0/meals/<meal_id>', methods=['DELETE'])
@is_admin
@token_required
def delete_meal_option(meal_id):
    """  file: apidocs/delete_meal.yml """
    meal = Meals.get_meal_by_id(meal_id)
    if not meal:
        return jsonify({'message':'Meal Not Found'}), 404
    meal.delete_meal()    
    return jsonify({'id': meal_id, 'message':'Meal Successfully Removed'}), 200    

@api_route.route('/bookmealapi/v1.0/meals', methods=['GET'])
@is_admin
@token_required
def get_all_meals():
    """ file: apidocs/get_meal.yml """
    meals = Meals.get_all_meals()
    output = []
    for meal in meals:
        meal_info = {}
        meal_info['id'] =  meal.id
        meal_info['meal_name'] =  meal.meal_name
        meal_info['price'] =  meal.price
        meal_info['meal_type'] =  meal.meal_type
        meal_info['created_at'] =  meal.created_at
        meal_info['updated_at'] =  meal.updated_at
        output.append(meal_info)    
    return jsonify({'meals': output}), 200
    
@api_route.route('/bookmealapi/v1.0/orders', methods=['GET'])
@is_admin
@token_required
def get_all_orders():
    """ file: apidocs/get_order.yml """
    orders = Orders.get_all_orders()
    output = []
    for order in orders:
        order_info = {}
        order_info['id'] =  order.id
        order_info['meal_name'] =  order.meal_name
        order_info['price'] =  order.price
        order_info['user_id'] =  order.user_id
        order_info['process_status'] =  order.process_status
        order_info['created_at'] =  order.created_at
        order_info['updated_at'] =  order.updated_at
        output.append(order_info)
    return jsonify({'transactions': output}), 200    

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

@api_route.route("/bookmealapi/v1.0/orders/<order_id>", methods=['DELETE'])
@token_required
def delete_order_item(order_id):
    """ file: apidocs/delete_order.yml """
    order = Orders.get_order_by_id(order_id)
    if not order:
        return jsonify({'message':'Meal Does Not Exist'}), 404
    order.delete_order()    
    return jsonify({'message':'Order Removed'}),200

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



    
