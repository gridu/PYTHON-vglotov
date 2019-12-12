from models.BookModel import *
from app import get_undefined


def test_book_addition():
    title = "Mother of wind" + datetime.now().isoformat()
    Book.add_book("Satire", title, "2019-11-11", None)
    assert Book.get_book_by_title(title).__len__() == 1
    Book.delete_book((Book.get_book_by_title(title)[0])['id'])


def test_book_deletion():
    title = "Mother of wind" + datetime.now().isoformat()
    Book.add_book("Satire", title, "2019-11-11", None)
    assert Book.get_book_by_title(title).__len__() == 1
    Book.delete_book((Book.get_book_by_title(title)[0])['id'])
    assert Book.get_book_by_title(title).__len__() == 0


def test_book_title_update():
    title = "Mother of wind" + datetime.now().isoformat()
    Book.add_book("Satire", title, "2019-11-05", None)
    assert Book.get_book_by_title(title).__len__() == 1
    book_id = (Book.get_book_by_title(title)[0])['id']
    new_title = "Father of wind" + datetime.now().isoformat()
    Book.rename_book(book_id, new_title)
    assert Book.get_book_by_title(title).__len__() == 0
    assert Book.get_book_by_title(new_title).__len__() == 1
    Book.delete_book((Book.get_book_by_title(new_title)[0])['id'])


def test_undefined_response_manipulation_get():
    response_body = json.loads(get_undefined().get_data().decode('utf8'))
    assert (response_body['error'].__eq__("No implementation for `GET` method"))


def test_limited_amount_of_latest_books():
    title = "Feathers"
    Book.add_book("Drama", title, "2019-12-11", None)
    Book.add_book("Satire", title, "2019-10-11", None)
    Book.add_book("Romance", title, "2019-09-11", None)
    latest_books = Book.get_latest_books(2)
    for book in latest_books:
        assert book['creation_date'] != "2019-09-11"
    for book_id in Book.get_ids_by_title(title):
        assert Book.delete_book(book_id[0])


def test_book_info_getting():
    title = "101 Dalmatians"
    new_title = "102 Parrots"
    Book.add_book("Drama", title, "2019-12-04", None)
    book_id = (Book.get_book_by_title(title)[0])['id']
    Book.rename_book(book_id, new_title)
    book = Book.get_book_by_id(book_id)[0]
    assert book['type'].__eq__("Drama")
    assert book['title'].__eq__(new_title)
    assert book['creation_date'].__eq__("2019-12-04")
    assert book['updated_date_time']
    Book.delete_book(book_id)


def test_get_all_ids_by_title():
    title = "Feathers" + datetime.now().isoformat()
    Book.add_book("Drama", title, "2019-12-11", None)
    Book.add_book("Satire", title, "2019-10-11", None)
    Book.add_book("Romance", "Butterfly", "2019-09-11", None)
    book1_id = (Book.get_book_by_title(title)[0])['id']
    book2_id = (Book.get_book_by_title(title)[1])['id']
    book3_id = (Book.get_book_by_title("Butterfly")[0])['id']
    book_ids_needed = []
    for book_id in Book.get_ids_by_title(title):
        book_ids_needed.append(book_id[0])
    assert book_ids_needed.__len__() == 2 and book1_id in book_ids_needed and book2_id in book_ids_needed
    assert (Book.get_book_by_title("Butterfly")[0])['id'] not in book_ids_needed
    for book_id in book_ids_needed:
        assert Book.delete_book(book_id)
    assert Book.delete_book(book3_id)


def test_all_books_getting():
    id_to_delete = []
    current_book_amount = Book.get_all_books().__len__()
    title = "Mother of wind" + datetime.now().isoformat()
    Book.add_book("Satire", title, "2019-11-11", None)
    id_to_delete.append((Book.get_book_by_title(title)[0])['id'])
    title = "Mother of wind" + datetime.now().isoformat()
    Book.add_book("Satire", title, "2019-11-03", None)
    id_to_delete.append((Book.get_book_by_title(title)[0])['id'])
    assert Book.get_all_books().__len__() == 2 + current_book_amount
    for book_id in id_to_delete:
        assert Book.delete_book(book_id)
