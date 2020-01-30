import pytest
import unittest

from models.BookModel import *
from db.Books_db import Books_db
from app import get_undefined

book_title = None


class BookTest1(unittest.TestCase):

    def setUp(self):
        self.book_title = 'Mother of wind' + datetime.now().isoformat()
        Books_db.add_book(Book('Satire', self.book_title, '2019-11-11', None))

    def tearDown(self):
        assert Books_db.delete_book(Book.get_book_by_title(self.book_title)[0]['id'])

    def test_book_addition(self):
        assert Book.get_book_by_title(self.book_title).__len__() == 1

    def test_book_title_update(self):
        assert Book.get_book_by_title(self.book_title).__len__() == 1
        book_id = (Book.get_book_by_title(self.book_title)[0])['id']
        new_title = 'Father of wind' + datetime.now().isoformat()
        Book.rename_book(book_id, new_title)
        assert Book.get_book_by_title(self.book_title).__len__() == 0
        assert Book.get_book_by_title(new_title).__len__() == 1
        self.book_title = new_title


class BookTest2(unittest.TestCase):

    def test_book_deletion(self):
        book_title = 'Mother of wind' + datetime.now().isoformat()
        Books_db.add_book(Book('Satire', book_title, '2019-11-11', None))
        assert Book.get_book_by_title(book_title).__len__() == 1
        assert Books_db.delete_book((Book.get_book_by_title(book_title)[0])['id'])
        assert Book.get_book_by_title(book_title).__len__() == 0

    def test_limited_amount_of_latest_books(self):
        title = 'Feathers'
        Books_db.add_book(Book('Drama', title, '2019-12-11', None))
        Books_db.add_book(Book('Satire', title, '2019-10-11', None))
        Books_db.add_book(Book('Romance', title, '2019-09-11', None))
        latest_books = Books_db.get_latest_books(2)
        for book in latest_books:
            assert book['creation_date'] != '2019-09-11'
        for book_id in Books_db.get_ids_by_title(title):
            assert Books_db.delete_book(book_id[0])

    def test_book_info_getting(self):
        title = '101 Dalmatians'
        new_title = '102 Parrots'
        Books_db.add_book(Book('Drama', title, '2019-12-04', None))
        book_id = (Book.get_book_by_title(title)[0])['id']
        Book.rename_book(book_id, new_title)
        book = Book.get_book_by_id(book_id)
        assert book['type'] == 'Drama'
        assert book['title'] == new_title
        assert book['creation_date'] == '2019-12-04'
        assert book['updated_date_time']
        assert Books_db.delete_book(book_id)

    def test_get_all_ids_by_title(self):
        title = 'Feathers' + datetime.now().isoformat()
        Books_db.add_book(Book('Drama', title, '2019-12-11', None))
        Books_db.add_book(Book('Satire', title, '2019-10-11', None))
        Books_db.add_book(Book('Romance', 'Butterfly', '2019-09-11', None))
        book1_id = (Book.get_book_by_title(title)[0])['id']
        book2_id = (Book.get_book_by_title(title)[1])['id']
        book3_id = (Book.get_book_by_title('Butterfly')[0])['id']
        book_ids_needed = []
        for book_id in Books_db.get_ids_by_title(title):
            book_ids_needed.append(book_id[0])
        assert book_ids_needed.__len__() == 2 and book1_id in book_ids_needed and book2_id in book_ids_needed
        assert (Book.get_book_by_title('Butterfly')[0])['id'] not in book_ids_needed
        for book_id in book_ids_needed:
            assert Books_db.delete_book(book_id)
        assert Books_db.delete_book(book3_id)

    def test_all_books_getting(self):
        id_to_delete = []
        current_book_amount = Books_db.get_all_books().__len__()
        title = 'Mother of wind' + datetime.now().isoformat()
        Books_db.add_book(Book('Satire', title, '2019-11-11', None))
        id_to_delete.append((Book.get_book_by_title(title)[0])['id'])
        title = 'Mother of wind' + datetime.now().isoformat()
        Books_db.add_book(Book('Satire', title, '2019-11-03', None))
        id_to_delete.append((Book.get_book_by_title(title)[0])['id'])
        assert Books_db.get_all_books().__len__() == 2 + current_book_amount
        for book_id in id_to_delete:
            assert Books_db.delete_book(book_id)


class BookTestWithoutLibraryUsage(unittest.TestCase):

    def test_zero_limit_value_raises_exception(self):
        with pytest.raises(ValueError):
            Books_db.get_latest_books(0)

    def test_negative_limit_value_raises_exception(self):
        with pytest.raises(ValueError):
            Books_db.get_latest_books(-2)

    def test_undefined_response_manipulation_get(self):
        response_body = json.loads(get_undefined().get_data().decode('utf8'))
        self.assertEqual('No implementation for `GET` method', response_body['error'])
