from flask_sqlalchemy import SQLAlchemy
import json
from db.settings import app
from datetime import datetime

db = SQLAlchemy(app)


class Book(db.Model):
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

    def get_all_books():
        return [Book.json(book) for book in Book.query.all()]

    def get_book_by_id(_id):
        return [Book.json(book) for book in Book.query.filter_by(id=_id)]

    def get_latest_books(_limit):
        if _limit <= 0:
            raise ValueError('Limit parameter should be >= 0')
        return [Book.json(book) for book in Book.query.order_by(Book.creation_date.desc()).limit(_limit)]

    def get_book_by_title(_title):
        return [Book.json(book) for book in Book.query.filter_by(title=_title)]

    def get_ids_by_title(_title):
        return [book for book in Book.query.with_entities(Book.id).filter_by(title=_title)]

    def delete_book(_id):
        is_successful = Book.query.filter_by(id=_id).delete()
        db.session.commit()
        return bool(is_successful)

    def rename_book(_id, _title):
        book_to_rename = Book.query.filter_by(id=_id).first()
        book_to_rename.title = _title
        book_to_rename.updated_date_time = datetime.now().isoformat()
        db.session.commit()
