from flask import Flask, jsonify, request, abort, session
from functools import wraps

app = Flask(__name__)

app.testing = True
app.secret_key = 'secret123'

users = [
    {
        'id': 1,
        'first_name': 'dennis',
        'last_name': 'lubega',
        'email': 'lubega@gmail.com',
        'password': '12345',
    },
    {
        'id': 2,
        'first_name': 'atlas',
        'last_name': 'Tegz',
        'email': 'atlas@gmail.com',
        'password': '12345',
    }
]

admin = {
    'id': 1,
    'business_name': 'HAPPY FOODS',
    'location': 'NAKULABYE',
    'first_name': 'steven',
    'last_name': 'walube',
    'email': 'steven@gmail.com',
    'password': '54321',
}

meals = [
    {
        'id': 1,
        'meal_name': "ricebeans",
        'price': 3000,
        'meal_type': "lunch"
    },
    {
        'id': 2,
        'meal_name': 'rolex',
        'price': 4000,
        'meal_type': 'lunch'
    }
]

# Need add date to this
transactions = [
    {
        'id': 1,
        'meal_name': "ricebeans",
        'price': 3000,
        'user_id': 1,
        'created_at': "2018-04-26 10:55:55.423844",
        'process_status': "pending"
    },
    {
        'id': 2,
        'meal_name': "lasagna",
        'price': 10000,
        'user_id': 2,
    },
    {
        'id': 3,
        'meal_name': 'rolex',
        'price': 4000,
        'user_id': 1,
    }
]

menu_day = [
    {
        'id': 1,
        'meal_name': "ricebeans",
        'price': 3000,
        'meal_type': "lunch"
    },
    {
        'id': 2,
        'meal_name': "lasagna",
        'price': 10000,
        'meal_type': "breakfast"
    },
    {
        'id': 3,
        'meal_name': "Rice and Matooke",
        'price': 10000,
        'meal_type': "lunch"
    },
    {
        'id': 4,
        'meal_name': 'rolex',
        'price': 4000,
        'meal_type': "lunch"
    }
]

# Check if user is logged


def is_loged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return jsonify({'message': "Unauthorized Access, Please Login"})
    return wrap

# Check if user


def is_user(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'userV' in session:
            return f(*args, **kwargs)
        else:
            return jsonify({'message': "Unauthorized Access, You are not an admin"})
    return wrap

# Check if Admin


def is_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin' in session:
            return f(*args, **kwargs)
        else:
            return jsonify({'message': "Unauthorized Access, You are not an admin"})
    return wrap


# Registering a User
@app.route('/bookmealapi/v1.0/auth/signup', methods=['POST'])
def sign_up():
    """ Regisrering User """
    if not request.get_json() or 'fname' not in request.get_json()\
    or 'lname' not in request.get_json() or 'email' not in request.get_json()\
    or 'password' not in request.get_json():
        abort(400)

    user_id = users[-1].get("id") + 1
    first_name = request.get_json().get('fname')
    last_name = request.get_json().get('lname')
    email = request.get_json().get('email')
    password = request.get_json().get('password')

    for user in users:
        if user["email"] == email:
            abort(400)

    user = {
        'id': user_id,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password,
    }

    users.append(user)
    return jsonify({'user': user, 'users': users}), 201

# Login


@app.route('/bookmealapi/v1.0/auth/login', methods=['POST'])
def login():
    """ login  """
    if not request.get_json() or 'email' not in request.get_json()\
     or 'password' not in request.get_json():
        abort(400)

    email = request.get_json().get('email')
    password = request.get_json().get('password')

    for user in users:
        if user['email'] == email:
            if user['password'] == password:
                session['logged_in'] = True
                session['userV'] = True
                return jsonify({'message': "Successfully login"}), 200
            else:
                return jsonify({'message': "Wrong Password", 'users': users}), 400

    if admin['email'] == email:
        if admin['password'] == password:
            session['logged_in'] = True
            session['admin'] = True
            return jsonify({'message': "Successfully login"}), 200
        else:
            return jsonify({'message': "Wrong Password", 'admin': admin}), 400

    return jsonify({'message': "User Not Found", 'users': users}), 400


# Add Meal
@app.route('/bookmealapi/v1.0/meals', methods=['POST'])
@is_loged_in
@is_admin
def add_meal():
    """ Adding meal  """
    if not request.get_json() or 'meal_name' not in request.get_json()\
    or 'price' not in request.get_json() or 'meal_type' not in request.get_json():
        abort(400)

    meal_name = request.get_json().get('meal_name')
    price = request.get_json().get('price')
    meal_type = request.get_json().get('meal_type')

    meal_id = meals[-1].get('id') + 1

    if type(price) is not int:
        abort(400)

    for meal in meals:
        if meal['meal_name'] == meal_name:
            abort(400)

    meal = {
        'id': meal_id,
        'meal_name': meal_name,
        'price': price,
        'meal_type': meal_type
    }

    meals.append(meal)
    return jsonify({'meal': meal}), 201

# Select Meal


@app.route('/bookmealapi/v1.0/orders', methods=['POST'])
@is_loged_in
@is_user
def select_meal():
    """ Selecting Meal """
    if not request.get_json() or 'meal_name' not in request.get_json()\
    or 'price' not in request.get_json() or 'userId' not in request.get_json():
        abort(400)
    meal_name = request.get_json().get('meal_name')
    price = request.get_json().get('price')
    user_id = request.get_json().get('userId')

    if type(price) is not int and type(user_id) is not int:
        abort(400)

    transaction_id = transactions[-1].get('id') + 1

    transaction = {
        'id': transaction_id,
        'meal_name': meal_name,
        'price': price,
        'user_id': user_id
    }
    transactions.append(transaction)
    return jsonify({'transaction': transaction}), 201


# set Meal Options
@app.route('/bookmealapi/v1.0/menu', methods=['POST'])
@is_loged_in
@is_admin
def set_menu():
    """ Setting menu """
    if not request.get_json():
        abort(400)
    meal_name = request.get_json().get('meal_name')
    price = request.get_json().get('price')
    meal_type = request.get_json().get('meal_type')

    meal = {
        "meal_name": meal_name,
        "price": price,
        "meal_type": meal_type
    }
    menu_day.append(meal)
    return jsonify({'menuDay': menu_day}), 201

  # update Meal Option


@app.route('/bookmealapi/v1.0/meals/<meal_id>', methods=['PUT'])
@is_loged_in
@is_admin
def update_meal_option(meal_id):
    """ Updating meals """
    if not request.get_json() or 'meal_name' not in request.get_json()\
    or 'meal_type' not in request.get_json():
        abort(400)
    meal_name = request.get_json().get('meal_name')
    price = request.get_json().get('price')
    meal_type = request.get_json().get('meal_type')

    if type(price) is not int:
        abort(400)

    for meal in meals:
        if meal['id'] == int(meal_id):
            meal['meal_name'] = meal_name
            meal['price'] = price
            meal['meal_type'] = meal_type
            return jsonify({'meal': meal}), 201
    abort(404)

# Modify Order


@app.route('/bookmealapi/v1.0/orders/<order_id>', methods=['PUT'])
@is_loged_in
def update_order(order_id):
    """ Modify Order """
    if not request.get_json() or 'meal_name' not in request.get_json()\
    or 'price' not in request.get_json():
        abort(400)

    meal_name = request.get_json().get('meal_name')
    price = request.get_json().get('price')

    if type(price) is not int:
        abort(400)

    for transaction in transactions:
        if transaction['id'] == int(order_id):
            transaction['meal_name'] = meal_name
            transaction['price'] = price
            return jsonify({'transaction': transaction}), 201
    abort(404)

# delete Meal Option


@app.route('/bookmealapi/v1.0/meals/<meal_id>', methods=['DELETE'])
@is_loged_in
@is_admin
def delete_meal_option(meal_id):
    """ Deleting Meal Option """
    for meal in meals:
        if meal['id'] == int(meal_id):
            meals.remove(meal)
            return jsonify({'Meals': meals}), 204
    return jsonify({'id': '' + meal_id}), 404

 # get all meals


@app.route('/bookmealapi/v1.0/meals', methods=['GET'])
@is_loged_in
@is_admin
def get_all_meals():
    """ Get all Meals """
    return jsonify({'meals': meals}), 200

  # get all orders


@app.route('/bookmealapi/v1.0/orders', methods=['GET'])
@is_loged_in
@is_admin
def get_all_orders():
    """ Get all orders """
    return jsonify({'transactions': transactions}), 200

# get menu of the day


@app.route('/bookmealapi/v1.0/menu', methods=['GET'])
@is_loged_in
@is_user
def get_menu():
    """ Get menu for the day """
    return jsonify({'menu_day': menu_day}), 200
