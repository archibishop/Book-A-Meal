from flask import Flask, jsonify, request, abort, session
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import datetime

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

app.config['SQLALCHEMY_DATABASE_URI'] =\
 "postgresql://postgres:12345@localhost/book"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

"""
Change to persistent data, using sql alchemy 
Using web tokens
Hashing Password sent to database

creating the models
"""

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))
    created_at = db.Column(db.DateTime(timezone=True),\
    default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True),\
    onupdate=datetime.datetime.utcnow)
    meal = db.relationship('Orders', backref='user', lazy=True)
    menu = db.relationship('Menu', backref='user', lazy=True)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business_name = db.Column(db.String(50))
    location = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))
    created_at = db.Column(db.DateTime(timezone=True),\
    default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True),\
    onupdate=datetime.datetime.utcnow)

class Meals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meal_name = db.Column(db.String(50), unique=True)
    price = db.Column(db.Integer)
    meal_type = db.Column(db.String(50))
    created_at = db.Column(db.DateTime(timezone=True),\
    default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True),\
    onupdate=datetime.datetime.utcnow)   

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


class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    meal_ids = db.Column(db.String(50))
    created_at = db.Column(db.DateTime(timezone=True),\
    default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True),\
    onupdate=datetime.datetime.utcnow)


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

    hashed_password = generate_password_hash(password, method='sha256')


    email_exists = User.query.filter_by(email=email).first()

    if email_exists != None:
        return jsonify({'message':'Email Already Exists'}), 400

    new_user = User(first_name= first_name, last_name=last_name,\
    email=email, password= hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message' : 'New user created!'}), 201

    """
    user_data = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': hashed_password,
    }
    message = user.add_user(user_data)

    if message == "Email Exists":
        return jsonify({'message':'Email Already Exists'}), 400
    else: 
        return jsonify({'meassage':'User Created','user': message}), 201
    """


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

    user = User.query.filter_by(email=email).first()

    if not user:
        admin = Admin.query.filter_by(email=email).first()

        if not admin:
            return jsonify({'message': 'User Not Found'}), 400

        if check_password_hash(admin.password, password):
            session['logged_in'] = True
            session['admin'] = True
            return jsonify({'message' : 'Successfully login'}), 200   
        else:
            return jsonify({'message':'Wrong Password'}), 400

    if check_password_hash(user.password, password):
        session['logged_in'] = True
        session['userV'] = True
        return jsonify({'message':'Successfully login'}), 200
    else:
        return jsonify({'message':'Wrong Password'}), 400                 

    """
    message_user = user.check_user_email_password(email, password)

    if message_user == True:
        session['logged_in'] = True
        session['userV'] = True
        return jsonify({'message': "Successfully login"}), 200
    else:
        message_admin = admin.check_admin_email_password(email, password)
        if message_admin == True:
            session['logged_in'] = True
            session['admin'] = True
            return jsonify({'message': "Successfully login"}), 200 
        else:
            return jsonify({'message': "User Not Found"}), 400
    """

""" Add Meal """
@app.route('/bookmealapi/v1.0/meals', methods=['POST'])
@is_loged_in
@is_admin
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

    if type(price) is not int:
        abort(400)    

    meal_exists = Meals.query.filter_by(meal_name=meal_name).first()

    if meal_exists != None:
        return jsonify({'message': "Meal Already Exists"}), 400

    meal = Meals(meal_name=meal_name, price=price, meal_type=meal_type)
    db.session.add(meal)
    db.session.commit()

    return jsonify({'message' : 'Meal Successfully Added'}), 201   

    """
    meal_name = request.get_json().get('meal_name')
    price = request.get_json().get('price')
    meal_type = request.get_json().get('meal_type')

    meal = {
       
        'meal_name': meal_name,
        'price': price,
        'meal_type': meal_type
    }

    meal_add = meals.add_meals(meal)
    if meal_add == "Successfully Added Meal":
        return jsonify({'message': "Meal Successfully Added"}), 201
    else:
        abort(400)  
    """      

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

    meal = Meals.query.filter_by(meal_name=meal_name).first()
    if not meal:
        return jsonify({'message': 'Meal Not Found'}), 400

    if type(price) is not int and type(user_id) is not int:
        abort(400)

    """
    transaction = {      
        'meal_name': meal_name,
        'price': price,
        'user_id': user_id
    }
    message_order = order.place_order(transaction)
    """
    process_status = "Pending"
    order = Orders(meal_name=meal_name, price=price, user_id=user_id, process_status=process_status)
    db.session.add(order)
    db.session.commit()

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

    """ Setting menu 
       We need to cocatenate the items in the lsit with a special character into a string
       And when retrieving it we return it into a string

    """
    
    if not request.get_json() or 'meal_ids' not in request.get_json()\
    or 'user_id' not in request.get_json():
        abort(400)
    """    
    meal_name = request.get_json().get('meal_name')
    price = request.get_json().get('price')
    meal_type = request.get_json().get('meal_type')
    """

    """ We need to check if the id exist in the meals"""

    meal_ids = request.get_json().get('meal_ids')
    user_id = request.get_json().get('user_id')

    if len(meal_ids) == 0:
        return jsonify({'message':'No meals sent for menu'}), 400
    """
    for meal_id in meal_ids:
        return jsonify({'message':'Testng Code'}), 400

    if meals.get_meals_name(meal_name) == "No Meals Found":
        return jsonify({'message':'Meal Does Not Exist'}), 404

    else:  
        menu = meals.update_meals_availability(meal_name)
    """

    caterer = Menu.query.filter_by(user_id=user_id).first()
    if caterer is not None:
        return jsonify({'message': 'Caterer Already Set Menu For the Day'}), 400
    
    meal_ids_string = ""
    for ids in meal_ids:
        meal_ids_string += ';%s' % ids 

    menu = Menu(user_id=user_id, meal_ids=meal_ids_string)
    db.session.add(menu)
    db.session.commit()

    menu_info = {}
    menu_info['id'] = menu.id
    menu_info['user_id'] = menu.user_id
    """ Converting the meal ids into a list again """
    converted_meal_ids = []
    for idx in menu.meal_ids.split(';'):
        if idx != "":
            converted_meal_ids.append(idx)

    menu_info['meal_ids'] = converted_meal_ids
    menu_info['created_at'] = menu.created_at
    menu_info['updated_at'] = menu.updated_at

    return jsonify({'message':'Menu Successfully Created',\
      'menu': menu_info}), 201            

    """
    menu_data = {
        'meal_ids': meal_ids,
        'user_id': user_id
    }
    menu_details = menu.add_meals_menu(menu_data)
    return jsonify({'message':'Menu Successfully Created',\
      'menu': menu_details}), 201
    """  


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


    meal = Meals.query.filter_by(id=meal_id).first()

    if not meal:
        return jsonify({'message':'Meal Does Not Exist'}), 400

    #Since mealName should be unqiue in the database Updating the same name causes Integrity Error
    if meal.meal_name != meal_name:
        meal.meal_name =  meal_name

    meal.price = price
    meal.meal_type = meal_type
    db.session.commit()

    meal_update = {}
    meal_update['id'] = meal.id
    meal_update['meal_name'] = meal.meal_name
    meal_update['price'] = meal.price
    meal_update['meal_type'] = meal.meal_type
    meal_update['created_at'] = meal.created_at
    meal_update['updated_at'] = meal.updated_at

    return jsonify({'message':'Meal Option Updated', 'meal':meal_update}), 201       
    """
    data = {
         'meal_name' : meal_name,
         'price' : price,
         'meal_type' : meal_type
    }    
    
    if meals.get_meals(int(meal_id)) == "No Meals Found":
        return jsonify({'message':'Meal Does Not Exist'}), 404

    meal = meals.update_meals(int(meal_id), data)
    return jsonify({'meal': meal}), 201
    """

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
    
    order = Orders.query.filter_by(id=order_id).first()

    if not order:
        return jsonify({'message':'Meal Does Not Exist'}), 404
    
    #Since mealName should be unqiue in the database Updating the same name causes Integrity Error
    if order.meal_name != meal_name:
        order.meal_name = meal_name

    order.price = price 
    db.session.commit()

    return jsonify({'message': 'Order Updated', 'order':order}), 201    
        
    """
    data = {
         'meal_name' : meal_name,  
         'price' : price 
    }     

    if order.get_order(int(order_id)) == "No Order Found":
        return jsonify({'message': "Meal Does Not Exist"}), 404
    else:      
        order_update = order.update_order(int(order_id), data)
        return jsonify({'order': order_update}), 201
    """


@app.route('/bookmealapi/v1.0/menu/<menu_id>', methods=['PUT'])
@is_loged_in
@is_admin
def update_menu(menu_id):

    
    """
     Reciving the string for meal_ids and spliting it 
    """    
    if not request.get_json() or 'meal_ids' not in request.get_json()\
    or 'user_id' not in request.get_json():
        abort(400)

    meal_ids = request.get_json().get('meal_ids')
    user_id = request.get_json().get('user_id')

    if type(user_id) is not int:
        abort(400)

    menu = Menu.query.filter_by(id=menu_id).first()
    if not menu:
        return jsonify({'message': 'Menu Does Not Exist'}), 404

    meal_ids_string = ""
    for ids in meal_ids:
        if ids != "":
           meal_ids_string += ';%s' % ids 

    menu.meal_ids = meal_ids_string
    db.session.commit()

    menu_info = {}
    menu_info['id'] = menu.id
    menu_info['user_id'] = menu.user_id
    """ Converting the meal ids into a list again """
    converted_meal_ids = []
    for idx in menu.meal_ids.split(';'):
        if idx != "":
            converted_meal_ids.append(idx)

    menu_info['meal_ids'] = converted_meal_ids
    menu_info['created_at'] = menu.created_at
    menu_info['updated_at'] = menu.updated_at

    return jsonify({'message': "Meal has been Updated in the menu",\
          'menu': menu_info}), 201

    """

    data = {
         'meal_ids' : meal_ids,  
         'user_id' : user_id  
    }     

    if menu.get_meal_menu(int(menu_id)) == "Menu Not Found":
        return jsonify({'message': "Menu Does Not Exist"}), 404
    else:      
        menu_update = menu.update_meal_menu(int(menu_id), data)
        return jsonify({'message': "Meal has been Updated in the menu",\
          'menu': menu_update}), 201 
    """                 

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

    meal = Meals.query.filter_by(id=meal_id).first()

    if not meal:
        return({'message':'Meal Not Found'}), 404

    db.session.delete(meal)
    db.session.commit()

    return jsonify({'id': '' + meal_id, 'message':'Meal Successfully Removed'}), 200    

            
    """        
    meal_id = int(meal_id)
    message_meal = meals.remove_meals(meal_id) 
    if message_meal == "Successfully Removed":
        return jsonify({'Meals': meals.get_all_meals()}), 200
    else:               
        return jsonify({'message':'Meal Not Found','id': ''+ str(meal_id)}), 404
    """

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

    meals = Meals.query.all()

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
    
    """
    return jsonify({'meals': meals.get_all_meals()}), 200
    """

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
    orders = Orders.query.all()

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

    
    """
    return jsonify({'transactions': order.get_all_orders()}), 200
    """
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
    menus = Menu.query.all()

    output = []

    for menu in menus:
        menu_info = {}
        menu_info['id'] = menu.id
        menu_info['user_id'] = menu.user_id
        """ Converting the meal ids into a list again """
        converted_meal_ids = []
        for idx in menu.meal_ids.split(';'):
            converted_meal_ids.append(idx)

        menu_info['meal_ids'] = converted_meal_ids
        menu_info['created_at'] = menu.created_at
        menu_info['updated_at'] = menu.updated_at
        output.append(menu_info)
    return jsonify({'menu_day': output}), 200

    """
    return jsonify({'menu_day': menu.get_full_menu()}), 200
    """


@app.route("/bookmealapi/v1.0/orders/<order_id>", methods=['DELETE'])
@is_loged_in
def delete_order_item(order_id):
    """ Documentation for deleting an order"""

    order = Orders.query.filter_by(id=order_id).first()

    if not order:
        return jsonify({'message':'Meal Does Not Exist'}), 404

    db.session.delete(order)
    db.session.commit()

    return jsonify({'message':'Order Removed'}),200

    """
    message = order.remove_order(int(order_id))
    if message == "No Order Found":
        return jsonify({'message':'Meal Does Not Exist'}), 404
    else:
        return jsonify({'message':'Order Removed'}), 200  
    """

@app.route("/bookmealapi/v1.0/menu/<menu_id>", methods=['DELETE'])
@is_loged_in
def delete_menu(menu_id):
    """ Documentation for deleting a menu"""

    menu = Menu.query.filter_by(id=menu_id).first()
    
    if not menu:
        return jsonify({'message':'Menu Does Not Exist'}), 404    
    
    db.session.delete(menu)
    db.session.commit() 
    return jsonify({'message':'Menu Successfully removed'}), 200
    """
    message = menu.remove_meal_menu(int(menu_id))
    if message == "Menu Not Found":
        return jsonify({'message':'Menu Does Not Exist'}), 404
    else:
        return jsonify({'message':'Menu Successfully removed'}), 200 
    """


    
