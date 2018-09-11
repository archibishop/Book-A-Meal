from flask import Flask, jsonify, request, abort, session, Blueprint, current_app
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import datetime
import jwt
from api import db
from .models.models import User, Menu, Order, Meal
from .utils import is_admin, token_required

api_auth = Blueprint("api_auth", __name__)


@api_auth.route('/bookmealapi/v1.0/auth/signup', methods=['POST'])
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
    return jsonify({'message': 'New user created!'}), 201


@api_auth.route('/bookmealapi/v1.0/auth/login', methods=['POST'])
def login():
    """ file: apidocs/user_login.yml  """
    data = request.get_json()
    response = User.validate_json_login(data)
    if response == "User Not Found":
        return jsonify({'message': response}), 404
    if response == "Wrong Password" or response == "Some values missing in json data sent":
        return jsonify({'message': response}), 400
    user = response
    role = ''
    if user.role_id == 2:
        session['is_user'] = True
        role = 'user'
    else:
        session['admin'] = True
        role = 'admin'
    token = jwt.encode({'id': user.id, 'role': role, 'exp': datetime.datetime.utcnow(
    ) + datetime.timedelta(minutes=30)}, current_app.config['SECRET_KEY'])
    return jsonify({'message': 'Successfully login', 'token': token.decode('UTF-8'), 'role': role, 'id': user.id}), 200
