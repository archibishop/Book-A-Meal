from flask import Flask, jsonify, request, abort, session
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import datetime
import jwt

from models.user import User
from models.admin import Admin
from models.meals import Meals
from models.order import Order
from models.menu import Menu
# from models.models import db

from utils import is_loged_in
from utils import is_user
from utils import is_admin
""" from utils import token_required """

from flasgger import Swagger

app = Flask(__name__)

app.testing = True
app.secret_key = 'secret123'

app.config['SQLALCHEMY_DATABASE_URI'] =\
 "postgres://bqvsyahcierxrk:7d270e10e8f11f9b3a00a86864927ec335ed11304e4e64bf47b7831f5e093b13@ec2-23-21-129-50.compute-1.amazonaws.com:5432/d54og171si9rmq"
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
    role_id = db.Column(db.Integer)
    business_name = db.Column(db.String(50))
    location = db.Column(db.String(50))
    created_at = db.Column(db.DateTime(timezone=True),\
    default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True),\
    onupdate=datetime.datetime.utcnow)
    meal = db.relationship('Orders', backref='user', lazy=True) 
    menu = db.relationship('Menu', backref='user', lazy=True)
    
    
"""
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
    menu = db.relationship('Menu', backref='admin', lazy=True)
"""    

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
    """
    user_id = db.Column(db.Integer)
    """
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

""" Web Token Authentication """

def token_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message' : 'Token is Invalid'}), 401

        return f(*args, **kwargs)
    return wrap


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
        description: Email Already Exists
      201:
        description: Successfully Registration
        schema:
          id: registermessage
          properties:
            message:
              type: string
              description: success message
              default: New user created!


    """
    """ Regisrering User """
    
    if not request.get_json() or 'fname' not in request.get_json()\
    or 'lname' not in request.get_json() or 'email' not in request.get_json()\
    or 'password' not in request.get_json() or 'role_id' not in request.get_json():
        abort(400)
    
    role_id = request.get_json().get('role_id')
    if role_id == 1:
        if 'business_name' not in request.get_json() \
              or 'location' not in request.get_json():
            abort(400)

    email = request.get_json().get('email')
    email_exists = User.query.filter_by(email=email).first()

    if email_exists != None:
        return jsonify({'message':'Email Already Exists'}), 400

    first_name = request.get_json().get('fname')
    last_name = request.get_json().get('lname')
    password = request.get_json().get('password')
    hashed_password = generate_password_hash(password, method='sha256')    
    
    if role_id == 2 :
        new_user = User(first_name= first_name, last_name=last_name,\
                      email=email, password= hashed_password, role_id=role_id)   
    else:
        new_user = User(first_name= first_name, last_name=last_name,\
                      email=email, password= hashed_password, role_id=role_id,\
                      business_name=business_name, location=location) 

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message' : 'New user created!'}), 201

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
      404:
        description: User Not Found
      400:
        description: Wrong Password    
      200:
        description: Successfully Login
        schema:
          id: awesome
          properties:
            message:
              type: string
              description: The language name
              default: Successfully login
            token:
              type: string
              description: The access token
              default: XIJSDF043-349329594 

    """
    """ login  """
    
    
    if not request.get_json() or 'email' not in request.get_json()\
     or 'password' not in request.get_json():
        abort(400)

    email = request.get_json().get('email')
    password = request.get_json().get('password')

    user = User.query.filter_by(email=email).first()
    
    if not user:
        return jsonify({'message': 'User Not Found'}), 404

    if check_password_hash(user.password, password):
        session['logged_in'] = True
        if user.role_id == 2:
            session['userV'] = True
        else:
            session['admin'] = True    
        token = jwt.encode({'id':user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'message':'Successfully login','token': token.decode('UTF-8')}), 200
    else:
        return jsonify({'message':'Wrong Password'}), 400                 

""" Add Meal """
@app.route('/bookmealapi/v1.0/meals', methods=['POST'])
@is_loged_in
@is_admin
@token_required
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
            created_at:
              type: string
              description: time created
              default: Fri, 04 May 2018 00:10:06 GMT
            updated_at:
              type: string
              description: time updated
              default: Fri, 04 May 2018 00:10:06 GMT    

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

""" Select Meal """
@app.route('/bookmealapi/v1.0/orders', methods=['POST'])
@is_loged_in
@token_required
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
      404:
        description: Meal Not Found
      404:
        description: Bad request 
      201:
        description: Order Made
        schema:
          id: select_meal_message
          properties:
            message:
              type: string
              description: order made
              default: Transaction Successfully Made
    """
    
    if not request.get_json() or 'meal_name' not in request.get_json()\
    or 'price' not in request.get_json() or 'userId' not in request.get_json():
        abort(400)
    meal_name = request.get_json().get('meal_name')
    price = request.get_json().get('price')
    user_id = request.get_json().get('userId')

    """
    Add check for if user id exists in the user table before it is added
    """

    if type(price) is not int and type(user_id) is not int:
        abort(400)

    meal = Meals.query.filter_by(meal_name=meal_name).first()
    if not meal:
        return jsonify({'message': 'Meal Not Found'}), 404

    process_status = "Pending"
    order = Orders(meal_name=meal_name, price=price, user_id=user_id, process_status=process_status)
    db.session.add(order)
    db.session.commit()

    return jsonify({'message': "Transacrtion Successfully Made"}), 201


""" set Meal Options """
@app.route('/bookmealapi/v1.0/menu', methods=['POST'])
@is_loged_in
@is_admin
@token_required
def set_menu():
    """
    Set Menu 
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
            - meal_ids
            - user_id
          properties:
            meal_ids:
              type: string
              description: meal name
              default: [1,3,5]
            user_id:
              type: integer
              description: user id
              default: 3 
    responses:
      400:
        description: 
      201:
        description: Order Made
        schema:
          id: menu
          properties:
            id:
              type: integer
              description: price for meal
              default: 3
            meal_ids:
              type: string
              description: meal ids
              default: [1,3,5]
            user_ids:
              type: integer
              description: user id
              default: 3 
            created_at:
              type: string
              description: time created menu
              default: Fri, 04 May 2018 00:10:06 GMT
            updated_at:
              type: string
              description: time updated menu
              default: Fri, 04 May 2018 00:10:06 GMT   

    """

    """ Setting menu 
       We need to cocatenate the items in the lsit with a special character into a string
       And when retrieving it we return it into a string

    """
    
    if not request.get_json() or 'meal_ids' not in request.get_json()\
    or 'user_id' not in request.get_json():
        abort(400)

    """ We need to check if the id exist in the meals"""

    meal_ids = request.get_json().get('meal_ids')
    user_id = request.get_json().get('user_id')

    if len(meal_ids) == 0:
        return jsonify({'message':'No meals sent for menu'}), 400

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
            converted_meal_ids.append(int(idx))

    menu_info['meal_ids'] = converted_meal_ids
    menu_info['created_at'] = menu.created_at
    menu_info['updated_at'] = menu.updated_at

    return jsonify({'message':'Menu Successfully Created',\
      'menu': menu_info}), 201              


@app.route('/bookmealapi/v1.0/meals/<meal_id>', methods=['PUT'])
@is_loged_in
@is_admin
@token_required
def update_meal_option(meal_id):
    """
    Update Meal Option
    BOOK-A-MEAL API
    Update meal
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
          id: update_meal
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
            created_at:
              type: string
              description: time created menu
              default: Fri, 04 May 2018 00:10:06 GMT
            updated_at:
              type: string
              description: time updated menu
              default: Fri, 04 May 2018 00:10:06 GMT  

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

""" Modify Order """
@app.route('/bookmealapi/v1.0/orders/<order_id>', methods=['PUT'])
@is_loged_in
@token_required
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
          properties:
            meal_name:
              type: string
              description: meal name
              default: spinach
            price:
              type: integer
              description: price for meal
              default: 2500 
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
            user_id:
              type: integer
              description: user id
              default: 1
            created_at:
              type: string
              description: time created menu
              default: Fri, 04 May 2018 00:10:06 GMT
            updated_at:
              type: string
              description: time updated menu
              default: Fri, 04 May 2018 00:10:06 GMT  

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

    output = {}
    output['id'] = order.id
    output['meal_name'] = order.meal_name
    output['price'] = order.price
    output['user_id'] = order.user_id
    output['created_at'] = order.created_at
    output['updated_at'] = order.updated_at

    return jsonify({'message': 'Order Updated', 'order': output}), 201    

@app.route('/bookmealapi/v1.0/menu/<menu_id>', methods=['PUT'])
@is_loged_in
@is_admin
@token_required
def update_menu(menu_id):
    """
    Update Menu
    BOOK-A-MEAL API
    update menu
    ---
    tags:
      - meals
    parameters:
      - in: body
        name: body
        schema:
          id: update_menu
          required:
            - meal_ids
            - user_id
          properties:
            meal_ids:
              type: string
              description: meal name
              default: [1,3,5]
            user_id:
              type: integer
              description: user id
              default: 3 
    responses:
      400:
        description: 
      201:
        description: Menu Updated
        schema:
          id: menu
          properties:
            id:
              type: integer
              description: price for meal
              default: 3
            meal_ids:
              type: string
              description: meal ids
              default: [1,3,5]
            user_ids:
              type: integer
              description: user id
              default: 3 
            created_at:
              type: string
              description: time created menu
              default: Fri, 04 May 2018 00:10:06 GMT
            updated_at:
              type: string
              description: time updated menu
              default: Fri, 04 May 2018 00:10:06 GMT   

    """
    
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
            converted_meal_ids.append(int(idx))

    menu_info['meal_ids'] = converted_meal_ids
    menu_info['created_at'] = menu.created_at
    menu_info['updated_at'] = menu.updated_at

    return jsonify({'message': "Meal has been Updated in the menu",\
          'menu': menu_info}), 201               

""" delete Meal Option """
@app.route('/bookmealapi/v1.0/meals/<meal_id>', methods=['DELETE'])
@is_loged_in
@is_admin
@token_required
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
          id: delete_message_meal
          properties:
            message:
              type: string
              description: delete message
              default: Meal Successfully Removed

    """
    """ Deleting Meal Option """

    meal = Meals.query.filter_by(id=meal_id).first()

    if not meal:
        return jsonify({'message':'Meal Not Found'}), 404

    db.session.delete(meal)
    db.session.commit()

    return jsonify({'id': meal_id, 'message':'Meal Successfully Removed'}), 200    

""" get all meals """
@app.route('/bookmealapi/v1.0/meals', methods=['GET'])
@is_loged_in
@is_admin
@token_required
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
                            'meal_type': "lunch",
                            'created_at': 'Fri, 04 May 2018 00:10:06 GMT',
                            'updated_at': 'Fri, 04 May 2018 00:10:06 GMT'
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
    

""" get all orders """
@app.route('/bookmealapi/v1.0/orders', methods=['GET'])
@is_loged_in
@is_admin
@token_required
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
                            'meal_type': "lunch",
                            'created_at': 'Fri, 04 May 2018 00:10:06 GMT',
                            'updated_at': 'Fri, 04 May 2018 00:10:06 GMT'
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

""" get menu of the day """
@app.route('/bookmealapi/v1.0/menu', methods=['GET'])
@is_loged_in
@token_required
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
                            'meal_ids':[1,2,3],
                            'user_id': 3,
                            'created_at': 'Fri, 04 May 2018 00:10:06 GMT',
                            'updated_at': 'Fri, 04 May 2018 00:10:06 GMT'
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
            if idx != "":
                converted_meal_ids.append(int(idx))

        menu_info['meal_ids'] = converted_meal_ids
        menu_info['created_at'] = menu.created_at
        menu_info['updated_at'] = menu.updated_at
        output.append(menu_info)
    return jsonify({'menu_day': output}), 200


@app.route("/bookmealapi/v1.0/orders/<order_id>", methods=['DELETE'])
@is_loged_in
@token_required
def delete_order_item(order_id):
    """
    delete an order
    BOOK-A-MEAL API
    delete order
    ---
    tags:
      - orders
    parameters:
    - name: order_id
      in: path
      type: integer
      required: true
      description: order id to be deleted
      default: 2
    responses:
      404:
        description: Order Not found
      200:
        description: Order Deleted 
        schema:
          id: delete_message_order
          properties:
            message:
              type: string
              description: delete message
              default: Order Removed

    """

    order = Orders.query.filter_by(id=order_id).first()

    if not order:
        return jsonify({'message':'Meal Does Not Exist'}), 404

    db.session.delete(order)
    db.session.commit()

    return jsonify({'message':'Order Removed'}),200


@app.route("/bookmealapi/v1.0/menu/<menu_id>", methods=['DELETE'])
@is_loged_in
@token_required
def delete_menu(menu_id):
    """ 
    delete menu 
    BOOK-A-MEAL API
    delete menu
    ---
    tags:
      - meals
    parameters:
    - name: menu_id
      in: path
      type: integer
      required: true
      description: menu id to be deleted
      default: 2
    responses:
      404:
        description: Menu Not found
      200:
        description: Menu Option Deleted
        schema:
          id: delete_message
          properties:
            message:
              type: string
              description: delete message
              default: Menu Successfully removed

    """

    menu = Menu.query.filter_by(id=menu_id).first()
    
    if not menu:
        return jsonify({'message':'Menu Does Not Exist'}), 404    
    
    db.session.delete(menu)
    db.session.commit() 
    return jsonify({'message':'Menu Successfully removed'}), 200



    
