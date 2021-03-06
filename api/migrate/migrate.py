from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =\
 "postgres://bqvsyahcierxrk:7d270e10e8f11f9b3a00a86864927ec335ed11304e4e64bf47b7831f5e093b13@ec2-23-21-129-50.compute-1.amazonaws.com:5432/d54og171si9rmq"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db =  SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

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

if __name__ == '__main__':
    manager.run()
