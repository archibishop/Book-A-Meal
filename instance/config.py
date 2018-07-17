import os

class Config(object):
    """ Parent Configuration file"""
    SECRET_KEY = "secret123"

class DevelopmentConfig(Config):
    """ Development Configuration file"""
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI", "postgresql://postgres:12345@localhost/book")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

class TestingConfig(Config):
    """ Testing Configuration file"""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URI", "postgresql://postgres:12345@localhost/test_book")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    """ Testing Configuration file"""
    TESTING = False
    DEBUG = False
    SQLALCHEMY_DATABASE_URL = os.environ.get(
        "DATABASE_URI", "postgresql://postgres:12345@localhost/test_book")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app_config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}    
