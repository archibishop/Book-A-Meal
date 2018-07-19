from functools import wraps
from flask import session, jsonify, request, current_app
import jwt

def is_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        " admin "
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

    



