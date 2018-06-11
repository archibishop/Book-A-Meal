from functools import wraps
from flask import session, jsonify, request, current_app
import jwt


""" Check if user is logged """

def is_loged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return jsonify({'message': "Unauthorized Access, Please Login"})
    return wrap

""" Check if user """


def is_user(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'userV' in session:
            return f(*args, **kwargs)
        else:
            return jsonify({'message': "Unauthorized Access,\
             You are not an admin"})
    return wrap

""" Check if Admin """


def is_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin' in session:
            return f(*args, **kwargs)
        else:
            return jsonify({'message':\
             "Unauthorized Access, You are not an admin"})
    return wrap


""" Web Token Authentication """


def token_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing'})

        try:
            # data = jwt.decode(token, app.config['SECRET_KEY'])
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Token is Invalid'}), 401

        return f(*args, **kwargs)
    return wrap

    



