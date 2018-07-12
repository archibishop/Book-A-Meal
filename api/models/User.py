from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from validate_email import validate_email
import datetime
from api import db
from werkzeug.security import generate_password_hash, check_password_hash

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
        if not self.first_name or not self.last_name\
                or not self.email or not self.password:
            return "Missing Values in Json Data sent"
        if not self.first_name.strip() or not self.last_name.strip()\
                or not self.email.strip() or not self.password.strip()\
                or not isinstance(self.role_id, int):
            return "Empty values missing in json data sent"
        if self.role_id == 1:
            if not self.business_name.strip() or not self.location.strip():
                return "Some values missing in json data sent"
            elif len(self.business_name) < 3 or len(self.location) < 3:
                return "Business name or location too short"
        else:
            self.business_name = ""
            self.location = ""
        if len(self.first_name) < 3 or len(self.last_name) < 3 or\
                len(self.password) < 5:
            return "Password/Firstname/lastname provided is too short."
        is_valid = validate_email(self.email)
        if not is_valid:
            return "Wrong Email Format Sent"
        email_exists = User.query.filter_by(email=self.email).first()
        if email_exists != None:
            return 'Email Already Exists'
        hashed_password = generate_password_hash(
            self.password, method='sha256')
        self.password = hashed_password
        return "Valid Data Sent"

    @staticmethod
    def validate_json_login(data):
        if data is None:
            return "No Data Sent"
        if 'email' not in data or 'password' not in data:
            return "Some values missing in json data sent"
        if data.get('email').strip() == '' or data.get('password').strip() == '':
            return "You sent some empty strings"
        user = User.get_user_email(data.get('email'))
        if user == "No User":
            return 'User Not Found'
        if not check_password_hash(user.password, data.get('password')):
            return "Wrong Password"
        return user
