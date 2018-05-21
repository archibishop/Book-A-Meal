from functools import wraps
from flask import session, jsonify, request
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

    



