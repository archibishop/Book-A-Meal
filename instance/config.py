import os

class Config(object):
    """ Parent Configuration file"""
    DEBUG = False
    DATABASE_URI = "postgresql://postgres:12345@localhost/book"
    SECRET_KEY = "secret123"

class DevelopmentConfig(Config):
    """ Development Configuration file"""
    DEBUG = True

class TestingConfig(Config):
    """ Testing Configuration file"""
    DEBUG = True
    DATABASE_URI = "postgresql: // postgres: 12345@localhost/test_book"

app_config = {
    "development ": DevelopmentConfig,
    "testing": TestingConfig
}    
