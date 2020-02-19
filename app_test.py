import unittest
from app import valid_book_object, valid_book_object_to_rename


class BookValidityCheckTest(unittest.TestCase):

    def test_valid_book_object_to_add_recognized(self):
        book = {
            'creation_date': '1998-10-11',
            'title': 'Pomi Dore',
            'type': 'Satire'
        }
        self.assertTrue(valid_book_object(book))

    def test_invalid_book_object_to_add_recognized(self):
        book = {
            'creation_date': '1998-10-11',
            'type': 'Pomi Dore'
        }
        self.assertFalse(valid_book_object(book))

    def test_valid_book_object_to_rename_recognized(self):
        book = {
            'id': 2,
            'title': 'Pomi Dore'
        }
        self.assertTrue(valid_book_object_to_rename(book))

    def test_invalid_book_object_to_rename_recognized(self):
        book = {
            'title': 'Pomi Dore'
        }
        self.assertFalse(valid_book_object_to_rename(book))
