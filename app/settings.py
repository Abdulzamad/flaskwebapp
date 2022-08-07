import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this-is-a-secret'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://admin:password@20.0.52.50/flask"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # https://testdriven.io/blog/flask-pytest/