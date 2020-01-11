import os

from flask import Flask, app
from flask_sqlalchemy import SQLAlchemy


class BaseConfig(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bookDB.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def create_app():
    application = Flask(__name__)
    application.config.from_object(BaseConfig)
    db = SQLAlchemy(application)
    db.init_app(application)
    return application

# app = Flask(__name__)

# def create_app(config=None):
#     # create and configure the app
#     application = Flask(__name__, instance_relative_config=True)
#     application.config.from_mapping(
#         SQLALCHEMY_DATABASE_URI='sqlite:///bookDB.db',
#         SQLALCHEMY_TRACK_MODIFICATIONS=False
#     )
#
#     if config is None:
#         # load the instance config, if it exists, when not testing
#         print(application.config.from_pyfile('config.py', silent=True))
#     else:
#         # load the test config if passed in
#         application.config.from_mapping(config)
#
#     return app
#
#
# app = create_app()

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookDB.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
