from db.settings import *

application = create_app()
DB = SQLAlchemy(application)


class Books_db(DB.Model):
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
        return {'id': self.id, 'type': self.type, 'title': self.title, 'creation_date': self.creation_date,
                'updated_date_time': self.updated_date_time}

    def add_book(self):
        DB.session.add(self)
        DB.session.commit()

    def delete_book(_id):
        is_successful = Books_db.query.filter_by(id=_id).delete()
        DB.session.commit()
        return bool(is_successful)

    def get_all_books():
        return [Books_db.json(book) for book in Books_db.query.all()]

    def get_ids_by_title(_title):
        return [_id for _id in Books_db.query.with_entities(Books_db.id).filter_by(title=_title)]

    def get_latest_books(_limit):
        if _limit <= 0:
            raise ValueError('Limit parameter should be > 0')
        return [Books_db.json(book) for book in Books_db.query.order_by(Books_db.creation_date.desc()).limit(_limit)]
