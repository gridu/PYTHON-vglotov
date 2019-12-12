import pytest

from models.BookModel import *

title = "Test book title"


@pytest.fixture
def addAndDeleteTestBook():
    Book.add_book("Satire", title, "2019-99-99")
    for book in Book.get_book_by_title(title): print(book['id'])
    # print(Book.get_book_by_title(title)(0)['id'])
    # yield Book.delete_book(Book.get_book_by_title(title)(0))


def test_bookAddition():
    Book.add_book("Satire", title, "2019-11-11", None)
    for book in Book.get_book_by_title(title): print(book['id'])
    assert Book.get_book_by_title(title).__len__() == 1
