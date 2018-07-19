from flask import Flask, jsonify, request, abort, session
from functools import wraps

from models.user import User
from models.admin import Admin
from models.meals import Meals
from models.order import Order
from models.menu import Menu

from utils import is_loged_in
from utils import is_user
from utils import is_admin

from flasgger import Swagger

app = Flask(__name__)

app.testing = True
app.secret_key = 'secret123'

Swagger(app)


@app.route('/bookmealapi/v1.0/auth/signup', methods=['POST'])
def sign_up():
    """
    file: apidocs/user_signup.yml
    """
    """ Regisrering User """    
    data = request.get_json()
    user = User(data.get('fname'), data.get(
        'lname'), data.get('email'), data.get('password'))
    response = user.validate_json()
    if response != "Valid Data Sent":
        return jsonify({'message': response}), 400
    user = user.add_user()
    user_data = {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'password': user.password
    }
    return jsonify({'meassage':'User Created','user': user_data}), 201

@app.route('/bookmealapi/v1.0/auth/login', methods=['POST'])
def login():
    """
    file: apidocs/user_login.yml
    """
    """ login  """
    data = request.get_json()
    response = User.validate_login(data)
    if response != "User":
        if response != "Admin":
            return jsonify({'message': response}), 400
    if response == "User":
        session['logged_in'] = True
        return jsonify({'message': "Successfully login"}), 200
    if response == "Admin":
        session['logged_in'] = True
        session['admin'] = True
        return jsonify({'message': "Successfully login"}), 200

@app.route('/bookmealapi/v1.0/meals', methods=['POST'])
@is_loged_in
def add_meal():
    """
    file: apidocs/add_meal.yml
    """
    """ Adding meal  """    
    data = request.get_json()
    meal = Meals(data.get('meal_name'), data.get(
        'price'), data.get('meal_type'), 0)
    response = meal.validate()
    if response != "Valid Data Sent":
        return jsonify({'message': response}), 400
    meal_add = meal.add_meals()
    return jsonify({'message': "Meal Successfully Added"}), 201
       

@app.route('/bookmealapi/v1.0/orders', methods=['POST'])
@is_loged_in
def select_meal():
    """
    file: apidocs/select_meal.yml
    """
    """ Selecting Meal """    
    data = request.get_json()
    order = Order(data.get('meal_name'), data.get('price'),\
            data.get('userId'))
    message = order.validate()
    if message != "Valid Data Sent":
        return jsonify({'message': message}), 400
    order.place_order()
    return jsonify({'message': "Transacrtion Successfully Made"}), 201

@app.route('/bookmealapi/v1.0/menu', methods=['POST'])
@is_loged_in
@is_admin
def set_menu():
    """
    file: apidocs/set_menu.yml
    """
    """ Setting menu """ 
    data = request.get_json()    
    menu = Menu(data.get("meal_ids"), data.get("user_id"))
    message = menu.validate()
    if message != "Valid Data Sent":
        return jsonify({"message": message}), 400
    menu_details = menu.add_meals_menu()
    menu_data = {
        'meal_ids': menu_details.meal_ids,
        'user_id': menu_details.user_id
    }
    return jsonify({'message':'Menu Successfully Created',\
      'menu': menu_data}), 201


@app.route('/bookmealapi/v1.0/meals/<meal_id>', methods=['PUT'])
@is_loged_in
@is_admin
def update_meal_option(meal_id):
    """
    file: apidocs/update_meal.yml
    """
    """ Updating meals """  
    data = request.get_json()
    message = Meals.validate_json(data)
    if message != "Valid Data Sent":
        return jsonify({"message":message}), 400
    data = {
        'meal_name': data.get('meal_name'),
        'price': data.get('price'),
        'meal_type': data.get('meal_type')
    }      
    if Meals.get_meals(int(meal_id)) == "No Meals Found":
        return jsonify({'message':'Meal Does Not Exist'}), 404
    meal = Meals.update_meals(int(meal_id), data)
    updated_meal = {
        'meal_name': meal.meal_name,
        'price': meal.price,
        'meal_type': meal.meal_type
    }
    return jsonify({'meal': updated_meal}), 201

@app.route('/bookmealapi/v1.0/orders/<order_id>', methods=['PUT'])
@is_loged_in
def update_order(order_id):
    """
    file: apidocs/update_order.yml
    """
    """ Modify Order """    
    data = request.get_json()
    message = Order.validate_json_1(data)
    if message != "Valid Data Sent":
        return jsonify({"message": message}), 400
    data = {
        'meal_name': data.get('meal_name'),
        'price': data.get('price')
    }     
    if Order.get_order(int(order_id)) == "No Order Found":
        return jsonify({'message': "Meal Does Not Exist"}), 404
    else:      
        order_update = Order.update_order(int(order_id), data)
        order = {
          'meal_name': order_update.meal_name,
          'price': order_update.price,
          'user_id': order_update.user_id
        }
        return jsonify({'order': order, "message": "Test"}), 201    

@app.route('/bookmealapi/v1.0/menu/<menu_id>', methods=['PUT'])
@is_loged_in
@is_admin
def update_menu(menu_id):
    """ 
    file: apidocs/update_menu.yml
    """
    data = request.get_json()
    message = Menu.validate_json(data)
    if message != "Valid Data Sent":
        return jsonify({'message': message}), 400
    data = {
        'meal_ids': data.get('meal_ids'),
        'user_id': data.get('user_id')
    }     
    if Menu.get_meal_menu(int(menu_id)) == "Menu Not Found":
        return jsonify({'message': "Menu Does Not Exist"}), 404
    else:      
        menu_update = Menu.update_meal_menu(int(menu_id), data)
        data = {
          "meal_ids": menu_update.meal_ids,
          "user_id": menu_update.user_id
        }
        return jsonify({'message': "Meal has been Updated in the menu",\
          'menu': data}), 201            

@app.route('/bookmealapi/v1.0/meals/<meal_id>', methods=['DELETE'])
@is_loged_in
@is_admin
def delete_meal_option(meal_id):
    """
    file: apidocs/delete_meal.yml
    """
    """ Deleting Meal Option """            
    meal_id = int(meal_id)
    message_meal = Meals.remove_meals(meal_id) 
    if message_meal == "Successfully Removed":
        return jsonify({'Meals': Meals.get_all_meals()}), 200
    else:               
        return jsonify({'message':'Meal Not Found','id': ''+ str(meal_id)}), 404

@app.route('/bookmealapi/v1.0/meals', methods=['GET'])
@is_loged_in
@is_admin
def get_all_meals():
    """
    file: apidocs/get_meal.yml
    """
    output = []
    meals = Meals.get_all_meals()
    for meal in meals:
        data = {
          'id': meal.id,
          'meal_name': meal.meal_name,
          'price': meal.price,
          'meal_type': meal.meal_type
        }
        output. append(data)
    return jsonify({'meals': output}), 200

@app.route('/bookmealapi/v1.0/orders', methods=['GET'])
@is_loged_in
@is_admin
def get_all_orders():
    """
    file: apidocs/get_order.yml
    """
    """ Get all orders """
    output = []
    orders = Order.get_all_orders()
    for order in orders:
        data = {
            'id': order.id,
            'meal_name': order.meal_name,
            'price': order.price,
            'meal_type': order.process_status
        }
        output. append(data)
    return jsonify({'transactions': output}), 200

@app.route('/bookmealapi/v1.0/menu', methods=['GET'])
@is_loged_in
def get_menu():
    """
    file: apidocs/get_menu.yml
    """
    """ Get menu for the day """
    output = []
    menus = Menu.get_full_menu()
    for menu in menus:
        data = {
            'id': menu.id,
            'meal_name': menu.meal_ids,
            'price': menu.user_id,
            'created_at': menu.created_at,
            'updated_at': menu.updated_at
        }
        output.append(data)
    return jsonify({'menu_day': output}), 200


@app.route("/bookmealapi/v1.0/orders/<order_id>", methods=['DELETE'])
@is_loged_in
def delete_order_item(order_id):
    """ 
    file: apidocs/delete_order.yml
    """
    message = Order.remove_order(int(order_id))
    if message == "No Order Found":
        return jsonify({'message':'Meal Does Not Exist'}), 404
    else:
        return jsonify({'message':'Order Removed'}), 200  

@app.route("/bookmealapi/v1.0/menu/<menu_id>", methods=['DELETE'])
@is_loged_in
def delete_menu(menu_id):
    """ 
    file: apidocs/delete_menu.yml
    """
    message = Menu.remove_meal_menu(int(menu_id))
    if message == "Menu Not Found":
        return jsonify({'message':'Menu Does Not Exist'}), 404
    else:
        return jsonify({'message':'Menu Successfully removed'}), 200 



    
