from flask import Flask
from flask_sqlalchemy import SQLAlchemy

database_name = 'bookDBtest.db'


class BaseConfig(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + database_name
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def create_app():
    _application = Flask(__name__)
    _application.config.from_object(BaseConfig)
    db = SQLAlchemy(_application)
    db.init_app(_application)
    return _application
