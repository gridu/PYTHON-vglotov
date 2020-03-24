import tempfile

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
database_name = 'bookDBtest.db'
temp_DB_dir = tempfile.mkdtemp()


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + temp_DB_dir + '/' + database_name
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(Config)
    db.init_app(app)
    print('this is after init app')

    with app.app_context():
        from . import routes

        # Create tables for our models
        db.create_all()
        print('this is after create All')

        return app

# database_name = 'bookDBtest.db'
# temp_DB_dir = tempfile.mkdtemp()
#
#
# class BaseConfig(object):
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///' + temp_DB_dir + '/' + database_name
#     SQLALCHEMY_TRACK_MODIFICATIONS = False


# def create_app():
#     _application = Flask(__name__)
#     _application.config.from_object(BaseConfig)
#     db = SQLAlchemy(_application)
#     db.init_app(_application)
#     return _application