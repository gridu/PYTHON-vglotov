This is a library app.
To start it - run './utils/runApp.txt' in terminal. It will install all needed requirements and create a database with
one table where book entries can be stored using next properties:

    id - assigned automatically
    type - type value is stored in ~enums/BookTypes.py enum
    title - book title
    creation_date - date when book added, user have to specify it
    updated_date_time - time when book title was updated, assigned automatically

Next methods are implemented:

    /v1/books/manipulation POST - Add book with no arguments but request payload as json contains fields (type, title, creation date)
    payload example:
    {
        "creation_date": "1998-10-11",
        "title": "Pomi Dore",
        "type": "Satire"
    }

    /v1/books/manipulation/<id> DELETE - Delete book with arguments (<id>)

    /v1/books/manipulation PUT - Change the name of the book with arguments (id)
    payload example:
    {
        "id": 2,
        "title": "Pomi Dore",
    }

    /v1/books/manipulation GET - Returns “No implementation for `GET` method”

    /v1/books/latest/<limit> GET - Get all the latest added books limited by some amount with arguments (<limit>)

    /v1/books/info/<id> GET - Get info(type, name etc …) about a book with arguments (<id>)

    /v1/books/ids GET - Get all ID of books by title with arguments (title)
    payload example:
    {
        "title": "Pomi Dore"
    }