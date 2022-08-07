import os
basedir = os.path.abspath(os.path.dirname(__file__))
from decouple import config

class Config(object):
    SECRET_KEY = config('SECRET_KEY') or 'this-is-a-secret'
    SQLALCHEMY_DATABASE_URI = config('DATABASE_URL') 
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # https://testdriven.io/blog/flask-pytest/