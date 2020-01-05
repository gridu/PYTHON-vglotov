from flask import Flask
from configuration import db_name, db_path
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:' + db_path + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

