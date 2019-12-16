import json
import logging

from flask import jsonify, request, Response
from models.BookModel import *
from enums.BookTypes import *
from db.settings import *
import argparse


logger = logging.getLogger()


def valid_book_object(book_object):
    available_types = []
    for book in BookType:
        available_types.append(book.value)
    return book_object.get('type') in available_types and 'title' in book_object \
           and 'creation_date' in book_object


def valid_book_object_to_rename(book_object):
    return 'id' in book_object and 'title' in book_object


@app.route('/v1/books')
def get_books():
    logger.info(' Gathering all books')
    return jsonify({'books': Book.get_all_books()})


@app.route('/v1/books/manipulation', methods=['GET'])
def get_undefined():
    invalid_book_err_msg = {
        'error': 'No implementation for `GET` method'
    }
    logger.info('Undefined route requested')
    return Response(json.dumps(invalid_book_err_msg), 400, mimetype='application/json')


@app.route('/v1/books/manipulation', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if valid_book_object(request_data):
        Book.add_book(request_data['type'], request_data['title'],
                      request_data['creation_date'], None)
        response = Response('', 201, mimetype='application/json')
        response.headers['Location'] = '/v1/books/info'
        logger.info(' Book with title ' + request_data['title'] + ' is added')
        return response

    invalid_book_err_msg = {
        'error': 'invalid object was passed in method',
        'help_string': 'follow the pattern'
    }
    response = Response(json.dumps(invalid_book_err_msg), 400, mimetype='application/json')
    logger.warning('Incorrect book format passed')
    return response


@app.route('/v1/books/info/<int:_id>')
def get_book(_id):
    return_value = Book.get_book_by_id(_id)
    logger.info('Get book with id = ' + str(_id))
    return jsonify(return_value)


@app.route('/v1/books/latest/<int:limit>', methods=['GET'])
def get_latest_books(limit):
    logger.info('Get latest book with amount limit = ' + str(limit))
    return jsonify({'books': Book.get_latest_books(limit)})


@app.route('/v1/books/ids', methods=['GET'])
def get_ids_by_title():
    book_list = Book.get_ids_by_title(request.get_json()['title'])
    book_list = [str(book_id[0]) for book_id in book_list]
    book_list = 'book_ids: ' + ', '.join(book_list)
    logger.info(' Get all book IDs with title = ' + request.get_json()['title'])
    return book_list


@app.route('/v1/books/manipulation', methods=['PUT'])
def rename_book():
    request_data = request.get_json()
    if not valid_book_object_to_rename(request_data):
        invalid_book_err_msg = {
            'error': 'There is no such book in library or used incorrect request data',
        }
        logger.warning('Fail on editing: there is no book with such ID')
        return Response(json.dumps(invalid_book_err_msg), status=400, mimetype='application/json')

    Book.rename_book(request_data['id'], request_data['title'])
    response = Response('', status=204, mimetype='application/json')
    logger.info(' Book with ID ' + str(request_data['id']) + ' is renamed to ' + request_data['title'])
    return response


@app.route('/v1/books/manipulation/<int:id>', methods=['DELETE'])
def delete_book(_id):
    if Book.delete_book(_id):
        logger.info(' Book with ID ' + str(_id) + ' is deleted')
        return Response('', 204)

    invalid_book_err_msg = {
        'error': 'There is no such book in library or used incorrect request data',
    }
    logger.warning('Failed to delete book')
    return Response(json.dumps(invalid_book_err_msg), 404, mimetype='application/json')


if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=5000, help='Port number')
    parser.add_argument('--log_method', type=str, default='console', help='Logging method')
    parser.add_argument('--log_lvl', type=str, default='INFO', help='Logging level')
    args = parser.parse_args()

    if args.log_method.__eq__('file'):
        fh = logging.FileHandler('app.logger')
    else:
        fh = logging.StreamHandler()
    fh.setLevel(logging.getLevelName(args.log_lvl))
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    db.create_all()
    app.run(port=args.port)
