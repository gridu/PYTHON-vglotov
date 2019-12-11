from flask import jsonify, request, Response
from models.BookModel import *
from enums.BookTypes import *
import json
import logging
import sys
from db.settings import *

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger()


def validBookObject(bookObject):
    available_types = []
    for book in BookType:
        available_types.append(book.value)
    if bookObject["type"] in available_types and "title" in bookObject:
        return True
    else:
        return False


def validBookObjectToRename(bookObject):
    if "id" in bookObject and "title" in bookObject:
        return True
    else:
        return False


@app.route('/books')
def get_books():
    log.info(' Gathering all books')
    return jsonify({'books': Book.get_all_books()})


@app.route('/v1/books/manipulation', methods=['GET'])
def get_undefined():
    invalidBookErrMsg = {
        "error": "No implementation for `GET` method"
    }
    log.info('Undefined route requested')
    return Response(json.dumps(invalidBookErrMsg), 400, mimetype='application/json')


@app.route('/v1/books/manipulation', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if validBookObject(request_data):
        Book.add_book(request_data['type'], request_data['title'], request_data['creation_date'], None)
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = "/v1/books/info"
        log.info(' Book with title "' + request_data['title'] + '" is added')
        return response
    else:
        invalidBookErrMsg = {
            "error": "invalid object was passed in method",
            "help_string": "follow the pattern"
        }
        response = Response(json.dumps(invalidBookErrMsg), 400, mimetype='application/json')
        log.warning('Incorrect book format passed')
        return response


@app.route('/v1/books/info')
def get_book():
    request_data = request.get_json()
    if 'id' in request_data:
        return_value = Book.get_book_by_id(request_data['id'])
        log_str = 'id ' + str(request_data['id'])
    if 'title' in request_data:
        return_value = Book.get_book_by_title(request_data['title'])
        log_str = 'title ' + request_data['title']
    log.info('Get book with ' + log_str)
    return jsonify(return_value)


@app.route('/v1/books/latest', methods=['GET'])
def get_latest_books():
    log.info('Get latest book with amount limit = ' + str(request.get_json()['limit']))
    return jsonify({'books': Book.get_latest_books(request.get_json()['limit'])})


@app.route('/v1/books/ids', methods=['GET'])
def get_ids_by_title():
    book_list = Book.get_ids_by_title(request.get_json()['title'])
    book_list = [str(book_id[0]) for book_id in book_list]
    book_list = 'book_ids: ' + ', '.join(book_list)
    log.info(' Get all book IDs with title = ' + request.get_json()['title'])
    return book_list


@app.route('/v1/books/manipulation', methods=['PUT'])
def rename_book():
    request_data = request.get_json()
    if not (validBookObjectToRename(request_data)):
        invalidBookErrMsg = {
            "error": "There is no such book in library or used incorrect request data",
        }
        log.warning('Fail on editing: there is no book with such ID')
        return Response(json.dumps(invalidBookErrMsg), status=400, mimetype='application/json')

    Book.rename_book(request_data['id'], request_data['title'])
    response = Response("", status=204, mimetype='application/json')
    log.info(' Book with ID ' + str(request_data['id']) + ' is renamed to "' + request_data['title'] + '"')
    return response


@app.route('/v1/books/manipulation', methods=['DELETE'])
def delete_book():
    request_data = request.get_json()
    if Book.delete_book(request_data['id']):
        log.info(' Book with ID ' + str(request_data['id']) + ' is deleted')
        return Response("", 204)

    invalidBookErrMsg = {
        "error": "There is no such book in library or used incorrect request data",
    }
    log.warning('Failed to delete book')
    return Response(json.dumps(invalidBookErrMsg), 404, mimetype='application/json')


if __name__ == "__main__":
    db.create_all()
    app.run(port=5000)
    Book.add_book(BookType.ROMANCE.value, "300 Spartans", "2019-11-11", None)
