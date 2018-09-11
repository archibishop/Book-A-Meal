from instance.config import app_config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger 
from flask_cors import CORS




db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    Swagger(app)

    app.debug = True
    app.secret_key = "secret123"
    db.init_app(app)

    """ Putting importation on because db instance had not been created before """
    from api.api import api_route
    from api.api_auth import api_auth
    from api.api_meal import api_meal
    from api.api_order import api_order
    app.register_blueprint(api_auth)
    app.register_blueprint(api_meal)
    app.register_blueprint(api_order)
    app.register_blueprint(api_route)

    return app

