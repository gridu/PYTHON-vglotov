
from flask_sqlalchemy import SQLAlchemy
from db.settings import app

db = SQLAlchemy(app)


class Books_db(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    title = db.Column(db.String(256), nullable=False)
    creation_date = db.Column(db.String(15), nullable=True)
    updated_date_time = db.Column(db.String(30), nullable=True)

    def __init__(self, book_type, title, creation_date, updated_date_time):
        self.type = book_type
        self.title = title
        self.creation_date = creation_date
        self.updated_date_time = updated_date_time

    def json(self):
        return {'id': self.id, 'type': self.type, 'title': self.title, 'creation_date': self.creation_date,
                'updated_date_time': self.updated_date_time}

    def add_book(self):
        db.session.add(self)
        db.session.commit()

    def delete_book(_id):
        is_successful = Books_db.query.filter_by(id=_id).delete()
        db.session.commit()
        return bool(is_successful)

    def get_all_books():
        return [Books_db.json(book) for book in Books_db.query.all()]

    def get_ids_by_title(_title):
        return [_id for _id in Books_db.query.with_entities(Books_db.id).filter_by(title=_title)]

    def get_latest_books(_limit):
        if _limit <= 0:
            raise ValueError('Limit parameter should be > 0')
        return [Books_db.json(book) for book in Books_db.query.order_by(Books_db.creation_date.desc()).limit(_limit)]
