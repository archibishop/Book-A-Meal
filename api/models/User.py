from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
import datetime
from api import db
from werkzeug.security import generate_password_hash, check_password_hash
import re

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))
    role_id = db.Column(db.Integer)
    business_name = db.Column(db.String(50))
    location = db.Column(db.String(50))
    created_at = db.Column(db.DateTime(timezone=True),
                           default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True),
                           onupdate=datetime.datetime.utcnow)
    meal = db.relationship('Orders', backref='user', lazy=True)
    menu = db.relationship('Menu', backref='user', lazy=True)

    def __init__(self, first_name, last_name, email, password, business_name, location, role_id):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.business_name = business_name
        self.location = location
        self.role_id = role_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_user_email(email):
        user = User.query.filter_by(email=email).first()
        if not user:
            return "No User"
        return user

    def validate(self):
        message, validation = '', True
        users = User.query.filter_by(email=self.email).all()
        if not self.first_name or not self.last_name\
                or not self.email or not self.password:
            message, validation = "Missing Values in Json Data sent", False
        elif not self.first_name.strip() or not self.last_name.strip()\
                or not self.email.strip() or not self.password.strip()\
                or not isinstance(self.role_id, int):
            message, validation = "Empty values missing in json data sent", False
        elif len(self.first_name) < 3 or len(self.last_name) < 3 or\
                len(self.password) < 5 or len(self.email) < 5:
            message, validation = "Password/Firstname/lastname provided is too short.", False
        elif len(self.first_name) > 30 or len(self.last_name) > 30 or\
                len(self.password) > 5 or len(self.email) > 30:
            message, validation = "Password/Firstname/lastname provided is too long.", False
        elif not self.validate_email(self.email):
            message, validation = "Wrong Email Format Sent", False
        elif User.query.filter_by(email=self.email).first():
            message, validation = 'Email Already Exists', False
        elif self.role_id == 1:
            if not self.business_name.strip() or not self.location.strip():
                message, validation = "Some values missing in json data sent", False
            elif len(self.business_name) < 3 or len(self.location) < 3:
                message, validation = "Business name or location too short", False
        elif self.role_id == 2:
            self.business_name = ""
            self.location = ""
        if not validation:
            return message    
        hashed_password = generate_password_hash(
            self.password, method='sha256')
        self.password = hashed_password
        return "Valid Data Sent"

    @staticmethod
    def validate_json_login(data):
        message, validation = '', True
        user = User.get_user_email(data.get('email'))
        if data is None:
            message, validation = "No Data Sent", False
        elif 'email' not in data or 'password' not in data:
            message, validation = "Some values missing in json data sent", False
        elif data.get('email').strip() == '' or data.get('password').strip() == '':
            message, validation = "You sent some empty strings", False
        elif user == "No User":
            message, validation = 'User Not Found', False
        elif not check_password_hash(user.password, data.get('password')):
            message, validation = "Wrong Password", False
        if not validation:
            return message    
        return user
 
    @staticmethod
    def validate_email(email):
        valid = re.match(
            r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email)
        if valid:
            return True    
        else:
            return False
