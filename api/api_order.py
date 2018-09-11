from flask import Flask, jsonify, request, abort, session, Blueprint, current_app
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import datetime
import jwt
from api import db
from .models.models import User, Menu, Order, Meal
from .utils import is_admin, token_required

api_order = Blueprint("api_order", __name__)


@api_order.route('/bookmealapi/v1.0/orders', methods=['POST'])
@token_required
def select_meal():
    """ file: apidocs/select_meal.yml """
    data = request.get_json()
    order = Order(meal_name=data.get('meal_name'),
                  user_id=data.get('user_id'), process_status="pending", admin_id=data.get('admin_id'))
    response = order.validate_json_object()
    if response != "Valid Data Sent":
        if response == "Meal Does Not Exist":
            return jsonify({'message': response}), 404
        else:
            return jsonify({'message': response}), 400
    order.save()
    return jsonify({'message': "Transacrtion Successfully Made"}), 201


@api_order.route('/bookmealapi/v1.0/orders', methods=['GET'])
@is_admin
@token_required
def get_all_orders():
    """ file: apidocs/get_order.yml """
    orders = Order.get_all_orders()
    output = get_order_list(orders)
    return jsonify({'transactions': output}), 200


@api_order.route('/bookmealapi/v1.0/orders/caterer/<caterer_id>', methods=['GET'])
@is_admin
@token_required
def get_orders_caterer(caterer_id):
    """ file: apidocs/get_order.yml """
    orders, total = Order.get_orders_by_admin_id(int(caterer_id))
    output = get_order_list(orders)
    return jsonify({'transactions': output, 'total': total}), 200


@api_order.route('/bookmealapi/v1.0/orders/<user_id>', methods=['GET'])
@token_required
def get_orders_user(user_id):
    orders = Order.get_order_by_user_id(user_id)
    output = get_order_list(orders)
    return jsonify({'transactions': output}), 200


@api_order.route("/bookmealapi/v1.0/orders/<order_id>", methods=['DELETE'])
@token_required
def delete_order_item(order_id):
    """ file: apidocs/delete_order.yml """
    order = Order.get_order_by_id(order_id)
    if not order:
        return jsonify({'message': 'Meal Does Not Exist'}), 404
    order.delete_order()
    return jsonify({'message': 'Order Removed'}), 200


def get_order_list(orders):
    output = []
    for order in orders:
        order_info = {}
        order_info['id'] = order.id
        order_info['meal_name'] = order.meal_name
        order_info['price'] = order.price
        order_info['user_id'] = order.user_id
        order_info['process_status'] = order.process_status
        order_info['created_at'] = order.created_at
        order_info['updated_at'] = order.updated_at
        order_info['admin_id'] = order.admin_id
        order_info['time_stamp'] = (int(order.created_at.timestamp()) * 1000)
        output.append(order_info)
    return output
