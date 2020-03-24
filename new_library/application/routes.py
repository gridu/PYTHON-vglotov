from flask import current_app as app, jsonify
import logging

from models import Books_db
from new_library.application import create_app

LOGGER = logging.getLogger()
app = create_app()


@app.route('/v1/books')
def get_books():
    LOGGER.info(' Gathering all books')
    return jsonify({'books': Books_db.json(book) for book in Books_db.query.all()})


if __name__ == '__main__':
    app.run(host='localhost')
