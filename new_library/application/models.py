from flask_sqlalchemy import SQLAlchemy

# from . import db

db = SQLAlchemy()


class Books_db(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    title = db.Column(db.String(256), nullable=False)
    creation_date = db.Column(db.String(15), nullable=True)
    updated_date_time = db.Column(db.String(30), nullable=True)

    def json(self):
        return {'id': self.id, 'type': self.type, 'title': self.title, 'creation_date': self.creation_date,
                'updated_date_time': self.updated_date_time}
