from flask import Flask, jsonify, request, abort, session, Blueprint, current_app
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import datetime
import jwt
from api import db
from .models.models import User, Menu, Order, Meal
from .utils import is_admin, token_required

api_meal = Blueprint("api_meal", __name__)


@api_meal.route('/bookmealapi/v1.0/meals', methods=['POST'])
@is_admin
@token_required
def add_meal():
    """ file: apidocs/add_meal.yml """
    data = request.get_json()
    meal = Meal(meal_name=data.get('meal_name'), price=data.get('price'),
                meal_type=data.get('meal_type'), admin_id=data.get('admin_id'))
    response = meal.validate_json()
    if response != "Valid Data Sent":
        return jsonify({'message': response}), 400
    meal.save()
    return jsonify({'message': 'Meal Successfully Added'}), 201


@api_meal.route('/bookmealapi/v1.0/meals', methods=['GET'])
@is_admin
@token_required
def get_all_meals():
    """ get meals """
    """ file: apidocs/get_meal.yml """
    meals = Meal.get_all_meals()
    output = get_meal_list(meals)
    return jsonify({'meals': output}), 200


@api_meal.route('/bookmealapi/v1.0/meals/<meal_id>', methods=['PUT'])
@is_admin
@token_required
def update_meal_option(meal_id):
    """ file: apidocs/update_meal.yml """
    data = request.get_json()
    response = Meal.update_meal(meal_id, data.get(
        'meal_name'), data.get('price'), data.get('meal_type'), data.get('admin_id'))
    if isinstance(response, str) and response != "Meal Does Not Exist":
        return jsonify({'message': "nothing"}), 400
    if response == "Meal Does Not Exist":
        return jsonify({'message': 'Meal Does Not Exist'}), 404
    meal = response
    meal_update = {}
    meal_update['id'] = meal.id
    meal_update['meal_name'] = meal.meal_name
    meal_update['price'] = meal.price
    meal_update['meal_type'] = meal.meal_type
    meal_update['created_at'] = meal.created_at
    meal_update['updated_at'] = meal.updated_at
    return jsonify({'message': 'Meal Option Updated', 'meal': meal_update}), 201


@api_meal.route('/bookmealapi/v1.0/meals/<meal_id>', methods=['DELETE'])
@is_admin
@token_required
def delete_meal_option(meal_id):
    """  file: apidocs/delete_meal.yml """
    meal = Meal.get_meal_by_id(meal_id)
    if not meal:
        return jsonify({'message': 'Meal Not Found'}), 404
    meal.delete_meal()
    return jsonify({'id': meal_id, 'message': 'Meal Successfully Removed'}), 200


@api_meal.route('/bookmealapi/v1.0/meals/<caterer_id>', methods=['GET'])
# @is_admin
@token_required
def get_meals_caterer(caterer_id):
    """ file: apidocs/get_meal.yml """
    meals = Meal.get_meals_by_admin_id(int(caterer_id))
    output = get_meal_list(meals)
    return jsonify({'meals': output}), 200


def get_meal_list(meals):
    output = []
    for meal in meals:
        meal_info = {}
        meal_info['id'] = meal.id
        meal_info['meal_name'] = meal.meal_name
        meal_info['price'] = meal.price
        meal_info['meal_type'] = meal.meal_type
        meal_info['created_at'] = meal.created_at
        meal_info['updated_at'] = meal.updated_at
        meal_info['admin_id'] = meal.admin_id
        output.append(meal_info)
    return output
