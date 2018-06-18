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

"""
user = User()
admin = Admin()
meals = Meals()
order = Order()
menu = Menu()
"""


Swagger(app)


""" Registering a User """
@app.route('/bookmealapi/v1.0/auth/signup', methods=['POST'])
def sign_up():
    """
    sign up
    BOOK-A-MEAL API
    Register a user
    ---
    tags:
      - user
    parameters:
      - in: body
        name: body
        schema:
          id: register
          required:
            - fname
            - lname
            - email
            - password
          properties:
            fname:
              type: string
              description: first name
              default: felix
            lname:
              type: string
              description: last name
              default: journey  
            email:
              type: string
              description: user email
              default: test@gmail.com
            password:
              type: string
              description: password
              default: "12345"
    responses:
      400:
        description: User Not Found
      201:
        description: Successfully Registration
        schema:
          id: registermessage
          properties:
            message:
              type: string
              description: success message
              default: User created


    """
    """ Regisrering User """
    
    if not request.get_json() or 'fname' not in request.get_json()\
    or 'lname' not in request.get_json() or 'email' not in request.get_json()\
    or 'password' not in request.get_json():
        abort(400)

    first_name = request.get_json().get('fname')
    last_name = request.get_json().get('lname')
    email = request.get_json().get('email')
    password = request.get_json().get('password')

    user_data = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password,
    }

    user = User(first_name, last_name, email, password)
    message = user.add_user()

    if message == "Email Exists":
        return jsonify({'message':'Email Already Exists'}), 400
    else: 
        user_data = {
            'id': message.id,
            'first_name': message.first_name,
            'last_name': message.last_name,
            'email': message.email,
            'password': message.password
        }
        return jsonify({'meassage':'User Created','user': user_data}), 201
           
""" Login """
@app.route('/bookmealapi/v1.0/auth/login', methods=['POST'])
def login():
    """
    login
    BOOK-A-MEAL API
    Send login credentials to api
    ---
    tags:
      - user
    parameters:
      - in: body
        name: body
        schema:
          id: login
          required:
            - email
            - password
          properties:
            email:
              type: string
              description: user email
              default: test@gmail.com
            password:
              type: string
              description: password
              default: "12345"
    responses:
      400:
        description: User Not Found
      200:
        description: Successfully Login
        schema:
          id: awesome
          properties:
            message:
              type: string
              description: The language name
              default: Successfully login

    """
    """ login  """
    
    
    if not request.get_json() or 'email' not in request.get_json()\
     or 'password' not in request.get_json():
        abort(400)

    email = request.get_json().get('email')
    password = request.get_json().get('password')

    
    """ message_user = user.check_user_email_password(email, password) """
    message_user = User.check_user_email_password(email, password)
    print(message_user)
    if message_user == True:
        session['logged_in'] = True
        session['userV'] = True
        return jsonify({'message': "Successfully login"}), 200
    else:
        message_admin = Admin.check_admin_email_password(email, password)
        print(message_admin)
        if message_admin == True:
            session['logged_in'] = True
            session['admin'] = True
            return jsonify({'message': "Successfully login"}), 200 
        else:
            return jsonify({'message': "User Not Found"}), 400


""" Add Meal """
@app.route('/bookmealapi/v1.0/meals', methods=['POST'])
@is_loged_in
# @is_admin
def add_meal():
    """
    add meal
    BOOK-A-MEAL API
    Adding meal
    ---
    tags:
      - meals
    parameters:
      - in: body
        name: body
        schema:
          id: add_meal
          required:
            - meal_name
            - price
            - meal_type
          properties:
            meal_name:
              type: string
              description: meal_name
              default: frenchbeans
            price:
              type: integer
              description: price for meal
              default: 5000 
            meal_type:
              type: string
              description: meal category
              default: lunch
    responses:
      400:
        description:
      201:
        description: Meal Added
        schema:
          id: adding_meal_message
          properties:
            id:
              type: integer
              description: price for meal
              default: 3
            meal_name:
              type: string
              description: meal_name
              default: frenchbeans
            price:
              type: integer
              description: price for meal
              default: 5000 
            meal_type:
              type: string
              description: meal category
              default: lunch

    """
    """ Adding meal  """
    
    if not request.get_json() or 'meal_name' not in request.get_json()\
    or 'price' not in request.get_json() or 'meal_type' not in request.get_json():
        abort(400)

    meal_name = request.get_json().get('meal_name')
    price = request.get_json().get('price')
    meal_type = request.get_json().get('meal_type')

    meal = { 
        'meal_name': meal_name,
        'price': price,
        'meal_type': meal_type
    }
    meal = Meals(meal_name, price, meal_type, 0)
    meal_add = meal.add_meals()
    if meal_add == "Successfully Added Meal":
        return jsonify({'message': "Meal Successfully Added"}), 201
    else:
        abort(400)    

""" Select Meal """


@app.route('/bookmealapi/v1.0/orders', methods=['POST'])
@is_loged_in

def select_meal():
    """
    select meal
    BOOK-A-MEAL API
    Selecting meal
    ---
    tags:
      - orders
    parameters:
      - in: body
        name: body
        schema:
          id: select_meal
          required:
            - meal_name
            - price
            - user_id
          properties:
            meal_name:
              type: string
              description: meal name
              default: katogo
            price:
              type: integer
              description: price for meal
              default: 3000 
            userId:
              type: integer
              description: user id
              default: 1
    responses:
      400:
        description: 
      201:
        description: Order Made
        schema:
          id: select_meal_message
          properties:
            id:
              type: integer
              description: price for meal
              default: 3
            meal_name:
              type: string
              description: mwal name
              default: katogo
            price:
              type: integer
              description: price for meal
              default: 3000 
            userId:
              type: integer
              description: user id
              default: 1

    """
    """ Selecting Meal """
    
    if not request.get_json() or 'meal_name' not in request.get_json()\
    or 'price' not in request.get_json() or 'userId' not in request.get_json():
        abort(400)
    meal_name = request.get_json().get('meal_name')
    price = request.get_json().get('price')
    user_id = request.get_json().get('userId')

    if type(price) is not int and type(user_id) is not int:
        abort(400)

    transaction = {      
        'meal_name': meal_name,
        'price': price,
        'user_id': user_id
    }
    order = Order(meal_name, price, user_id)
    message_order = order.place_order()
    return jsonify({'message': "Transacrtion Successfully Made"}), 201


""" set Meal Options """
@app.route('/bookmealapi/v1.0/menu', methods=['POST'])
@is_loged_in
@is_admin
def set_menu():
    """
    setting meal
    BOOK-A-MEAL API
    Set menu for the day
    ---
    tags:
      - meals
    parameters:
      - in: body
        name: body
        schema:
          id: set_menu
          required:
            - meal_name
            - price
            - user_id
          properties:
            meal_name:
              type: string
              description: meal name
              default: katogo
            price:
              type: integer
              description: price for meal
              default: 3000 
            meal_type:
              type: string
              description: meal type
              default: breakfast
    responses:
      400:
        description: 
      201:
        description: Order Made
        schema:
          id: set_menu_message
          properties:
            id:
              type: integer
              description: price for meal
              default: 3
            meal_name:
              type: string
              description: mwal name
              default: katogo
            price:
              type: integer
              description: price for meal
              default: 3000 
            meal_type:
              type: string
              description: meal type
              default: brakfast

    """
    """ Setting menu """
    
    if not request.get_json() or 'meal_ids' not in request.get_json()\
    or 'user_id' not in request.get_json():
        abort(400)
 

    """ We need to check if the id exist in the meals"""

    meal_ids = request.get_json().get('meal_ids')
    user_id = request.get_json().get('user_id')

    if len(meal_ids) == 0:
        return jsonify({'message':'No meals sent for menu'}), 400
    
    menu = Menu(meal_ids, user_id)
    menu_details = menu.add_meals_menu()
    menu_data = {
        'meal_ids': menu_details.meal_ids,
        'user_id': menu_details.user_id
    }
    print(menu_data)
    return jsonify({'message':'Menu Successfully Created',\
      'menu': menu_data}), 201


@app.route('/bookmealapi/v1.0/meals/<meal_id>', methods=['PUT'])
@is_loged_in
@is_admin
def update_meal_option(meal_id):
    """
    Update Meal Option
    BOOK-A-MEAL API
    Set menu for the day
    ---
    tags:
      - meals
    parameters:
      - name: meal_id
        in: path
        type: integer
        required: true
        description: meal option to be modified
        default: 2
      - in: body
        name: body
        schema:
          id: update_meal_option
          required:
            - meal_name
            - price
            - user_id
          properties:
            meal_name:
              type: string
              description: meal name
              default: katogo
            price:
              type: integer
              description: price for meal
              default: 3000 
            meal_type:
              type: string
              description: meal type
              default: breakfast
    responses:
      400:
        description: 
      201:
        description: Meal Updated
        schema:
          id: update_meal_message
          properties:
            id:
              type: integer
              description: price for meal
              default: 3
            meal_name:
              type: string
              description: mwel name
              default: katogo
            price:
              type: integer
              description: price for meal
              default: 3000 
            meal_type:
              type: string
              description: meal type
              default: breakfast

    """
    """ Updating meals """
    
    if not request.get_json() or 'meal_name' not in request.get_json()\
    or 'meal_type' not in request.get_json():
        abort(400)
    meal_name = request.get_json().get('meal_name')
    price = request.get_json().get('price')
    meal_type = request.get_json().get('meal_type')

    if type(price) is not int:
        abort(400)

    data = {
         'meal_name' : meal_name,
         'price' : price,
         'meal_type' : meal_type
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

""" Modify Order """


@app.route('/bookmealapi/v1.0/orders/<order_id>', methods=['PUT'])
@is_loged_in
def update_order(order_id):
    """
    Modify order
    BOOK-A-MEAL API
    modify order
    ---
    tags:
      - orders
    parameters:
      - name: order_id
        in: path
        type: integer
        required: true
        description: oder to be modified
        default: 2
      - in: body
        name: body
        schema:
          id: modify_order
          required:
            - meal_name
            - price
            - user_id
          properties:
            meal_name:
              type: string
              description: meal name
              default: spinach
            price:
              type: integer
              description: price for meal
              default: 2500 
            meal_type:
              type: string
              description: meal type
              default: lunch
    responses:
      400:
        description: 
      201:
        description: Order Modified
        schema:
          id: set_menu_message
          properties:
            id:
              type: integer
              description: price for meal
              default: 3
            meal_name:
              type: string
              description: meal name
              default: katogo
            price:
              type: integer
              description: price for meal
              default: 3000 
            meal_type:
              type: string
              description: meal type
              default: breakfast

    """
    """ Modify Order """
    
    if not request.get_json() or 'meal_name' not in request.get_json()\
    or 'price' not in request.get_json():
        abort(400)

    meal_name = request.get_json().get('meal_name')
    price = request.get_json().get('price')

    if type(price) is not int:
        abort(400)

    data = {
         'meal_name' : meal_name,  
         'price' : price 
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
    
    if not request.get_json() or 'meal_ids' not in request.get_json()\
    or 'user_id' not in request.get_json():
        abort(400)

    meal_ids = request.get_json().get('meal_ids')
    user_id = request.get_json().get('user_id')

    if type(user_id) is not int:
        abort(400)

    data = {
         'meal_ids' : meal_ids,  
         'user_id' : user_id  
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

""" delete Meal Option """
@app.route('/bookmealapi/v1.0/meals/<meal_id>', methods=['DELETE'])
@is_loged_in
@is_admin
def delete_meal_option(meal_id):
    """
    delete meal option
    BOOK-A-MEAL API
    delete meal option
    ---
    tags:
      - meals
    parameters:
    - name: meal_id
      in: path
      type: integer
      required: true
      description: meal id to be deleted
      default: 2
    responses:
      404:
        description: Meal Not found
      200:
        description: Meal Option Deleted
        schema:
          id: delete_message
          properties:
            id:
              type: integer
              description: meal id
              default: 3

    """
    """ Deleting Meal Option """
            
    meal_id = int(meal_id)
    message_meal = Meals.remove_meals(meal_id) 
    if message_meal == "Successfully Removed":
        return jsonify({'Meals': Meals.get_all_meals()}), 200
    else:               
        return jsonify({'message':'Meal Not Found','id': ''+ str(meal_id)}), 404

""" get all meals """


@app.route('/bookmealapi/v1.0/meals', methods=['GET'])
@is_loged_in
@is_admin
def get_all_meals():
    """
    Get all meals
    BOOK-A-MEAL API
    Call this api url and it will return the all the meals in the system
    ---
    tags:
      - meals
    responses:
      500:
        description: Error The language is not awesome!
      200:
        description: All meals returned
        schema:
          id: meal
          properties:
            meals:
              type: array
              description: The awesomeness list
              items:
                type: string
              default: [{
                            'id': 1,
                            'meal_name': "ricebeans",
                            'price': 3000,
                            'meal_type': "lunch"
                        }]

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

""" get all orders """


@app.route('/bookmealapi/v1.0/orders', methods=['GET'])
@is_loged_in
@is_admin
def get_all_orders():
    """
    Get all orders
    BOOK-A-MEAL API
    All the orders in the system
    ---
    tags:
      - orders
    responses:
      400:
        description:  
      200:
        description: All meals returned
        schema:
          id: order
          properties:
            orders:
              type: array
              description: TA ll orders
              items:
                type: string
              default: [{
                            'id': 1,
                            'meal_name': "ricebeans",
                            'price': 3000,
                            'meal_type': "lunch"
                        }]

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

""" get menu of the day """


@app.route('/bookmealapi/v1.0/menu', methods=['GET'])
@is_loged_in
def get_menu():
    """
    Get menu for the day
    BOOK-A-MEAL API
    Call this api url and it will return the menu for the day
    ---
    tags:
      - meals
    responses:
      400:
        description: 
      200:
        description: menu returned
        schema:
          id: menu_day
          properties:
            menu:
              type: array
              description: The awesomeness list
              items:
                type: string
              default: [{
                            'id': 1,
                            'meal_name': "ricebeans",
                            'price': 3000,
                            'meal_type': "lunch"
                        }]

    """
    """ Get menu for the day """
    
    # return jsonify({'menu_day': meals.menu_meals()}), 200
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
    """ Documentation for deleting an order"""
    message = Order.remove_order(int(order_id))
    if message == "No Order Found":
        return jsonify({'message':'Meal Does Not Exist'}), 404
    else:
        return jsonify({'message':'Order Removed'}), 200  

@app.route("/bookmealapi/v1.0/menu/<menu_id>", methods=['DELETE'])
@is_loged_in
def delete_menu(menu_id):
    """ Documentation for deleting a enu"""
    message = Menu.remove_meal_menu(int(menu_id))
    if message == "Menu Not Found":
        return jsonify({'message':'Menu Does Not Exist'}), 404
    else:
        return jsonify({'message':'Menu Successfully removed'}), 200 



    
