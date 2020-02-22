from datetime import datetime
from db.settings import *

from enums.BookTypes import BookType

APPLICATION = create_app()
DB = SQLAlchemy(APPLICATION)


def valid_book_object(book_object):
    """
    Method checks whether passed parameter is valid book object to create.

    Args:
        book_object (json): book object to create in DB.

    Returns:
        bool: True for valid object, False otherwise.
    """
    available_types = []
    for book in BookType:
        available_types.append(book.value)
    return book_object.get('type') in available_types and 'title' in book_object \
           and 'creation_date' in book_object


def valid_book_object_to_rename(book_object):
    return 'id' in book_object and 'title' in book_object


class Book(DB.Model):
    __tablename__ = 'books'
    id = DB.Column(DB.Integer, primary_key=True)
    type = DB.Column(DB.String(50))
    title = DB.Column(DB.String(256), nullable=False)
    creation_date = DB.Column(DB.String(15), nullable=True)
    updated_date_time = DB.Column(DB.String(30), nullable=True)

    def __init__(self, book_type, title, creation_date, updated_date_time):
        self.type = book_type
        self.title = title
        self.creation_date = creation_date
        self.updated_date_time = updated_date_time

    def json(self):
        return {'id': self.id, 'type': self.type, 'title': self.title,
                'creation_date': self.creation_date, 'updated_date_time': self.updated_date_time}

    def get_book_by_id(_id):
        return Book.json(Book.query.filter_by(id=_id).one())

    def get_book_by_title(_title):
        return [Book.json(book) for book in Book.query.filter_by(title=_title)]

    def get_ids_by_title(_title):
        return [book for book in Book.query.with_entities(Book.id).filter_by(title=_title)]

    def delete_book(_id):
        is_successful = Book.query.filter_by(id=_id).delete()
        DB.session.commit()
        return bool(is_successful)

    def rename_book(_id, _title):
        book_to_rename = Book.query.filter_by(id=_id).first()
        book_to_rename.title = _title
        book_to_rename.updated_date_time = datetime.now().isoformat()
        DB.session.commit()


DB.create_all()
DB.session.commit()
