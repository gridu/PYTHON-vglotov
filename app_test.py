from app import valid_book_object, valid_book_object_to_rename


def test_valid_book_object_to_add_recognized():
    book = {
        'creation_date': '1998-10-11',
        'title': 'Pomi Dore',
        'type': 'Satire'
    }
    assert valid_book_object(book)


def test_invalid_book_object_to_add_recognized():
    book = {
        'creation_date': '1998-10-11',
        'type': 'Pomi Dore'
    }
    assert not valid_book_object(book)


def test_valid_book_object_to_rename_recognized():
    book = {
        'id': 2,
        'title': 'Pomi Dore'
    }
    assert valid_book_object_to_rename(book)


def test_invalid_book_object_to_rename_recognized():
    book = {
        'title': 'Pomi Dore'
    }
    assert not valid_book_object_to_rename(book)
