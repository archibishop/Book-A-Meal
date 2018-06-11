from instance.config import app_config
from api import create_app, db
from flask import current_app

app = create_app("development")

if __name__ == '__main__': 
    app.run()
