"""
This module runs the library with no books in it.
"""

import argparse
import logging
import json

from flask import jsonify, request, Response

from db.Books_db import *
from models.BookModel import *

LOGGER = logging.getLogger()
APPLICATION = create_app()


@APPLICATION.route('/v1/books')
def get_books():
    LOGGER.info(' Gathering all books')
    return jsonify({'books': Books_db.get_all_books()})


@APPLICATION.route('/v1/books/manipulation', methods=['GET'])
def get_undefined():
    invalid_book_err_msg = {
        'error': 'No implementation for `GET` method'
    }
    LOGGER.info('Undefined route requested')
    return Response(json.dumps(invalid_book_err_msg), 400, mimetype='application/json')


@APPLICATION.route('/v1/books/manipulation', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if valid_book_object(request_data):
        Books_db.add_book(Books_db(request_data['type'], request_data['title'],
                                   request_data['creation_date'], None))
        response = Response('', 201, mimetype='application/json')
        response.headers['Location'] = '/v1/books/info'
        LOGGER.info('Book with title %s is added', request_data['title'])
        return response

    invalid_book_err_msg = {
        'error': 'invalid object was passed in method',
        'help_string': 'follow the pattern'
    }
    response = Response(json.dumps(invalid_book_err_msg), 400, mimetype='application/json')
    LOGGER.warning('Incorrect book format passed')
    return response


@APPLICATION.route('/v1/books/info/<int:_id>')
def get_book(_id):
    return_value = Book.get_book_by_id(_id)
    LOGGER.info('Get book with id = %s', str(_id))
    return return_value


@APPLICATION.route('/v1/books/latest/<int:limit>', methods=['GET'])
def get_latest_books(limit):
    LOGGER.info('Get latest book with amount limit = %s', str(limit))
    return jsonify({'books': Books_db.get_latest_books(limit)})


@APPLICATION.route('/v1/books/ids', methods=['GET'])
def get_ids_by_title():
    book_list = Books_db.get_ids_by_title(request.get_json()['title'])
    book_list = [str(book_id[0]) for book_id in book_list]
    book_list = 'book_ids: ' + ', '.join(book_list)
    LOGGER.info(' Get all book IDs with title = %s', request.get_json()['title'])
    return book_list


@APPLICATION.route('/v1/books/manipulation', methods=['PUT'])
def rename_book():
    request_data = request.get_json()
    if not valid_book_object_to_rename(request_data):
        invalid_book_err_msg = {
            'error': 'There is no such book in library or used incorrect request data',
        }
        LOGGER.warning('Fail on editing: there is no book with such ID')
        return Response(json.dumps(invalid_book_err_msg), status=400, mimetype='application/json')

    Book.rename_book(request_data['id'], request_data['title'])
    response = Response('', status=204, mimetype='application/json')
    LOGGER.info(' Book with ID %s is renamed to %s', str(request_data['id']), request_data['title'])
    return response


@APPLICATION.route('/v1/books/manipulation/<int:_id>', methods=['DELETE'])
def delete_book(_id):
    if Books_db.delete_book(_id):
        LOGGER.info(' Book with ID %s is deleted', str(_id))
        return Response('', 204)

    invalid_book_err_msg = {
        'error': 'There is no such book in library or used incorrect request data',
    }
    LOGGER.warning('Failed to delete book')
    return Response(json.dumps(invalid_book_err_msg), 404, mimetype='application/json')


if __name__ == '__main__':
    LOGGER.setLevel(logging.DEBUG)
    FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('--port', type=int, default=5000, help='Port number')
    PARSER.add_argument('--log_method', type=str, default='console', help='Logging method')
    PARSER.add_argument('--log_lvl', type=str, default='INFO', help='Logging level')
    ARGS = PARSER.parse_args()

    if ARGS.log_method == 'file':
        HANDLER = logging.FileHandler('log/app.logger')
    else:
        HANDLER = logging.StreamHandler()
    HANDLER.setLevel(logging.getLevelName(ARGS.log_lvl))
    HANDLER.setFormatter(FORMATTER)
    LOGGER.addHandler(HANDLER)

    APPLICATION.run(port=ARGS.port)
