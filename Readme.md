# Library app
Execute next script to start app:
```sh
$ ./install/runApp.txt
```
This will install all needed requirements and create a database with one table where book entries can be stored using next properties:

    id - assigned automatically
    type - type value is stored in ~enums/BookTypes.py enum
    title - book title
    creation_date - date when book added, user have to specify it
    updated_date_time - time when book title was updated, assigned automatically

### Methods implemented:
- Add book with no arguments but request payload as json contains fields (type, title, creation date):
    
        /v1/books/manipulation POST 
    
    payload example:

        {
            "creation_date": "1998-10-11",
            "title": "Pomi Dore",
            "type": "Satire"
        }

- Delete book with arguments (<id>)

        /v1/books/manipulation/<id> DELETE  

- Change the name of the book with arguments (id)

        /v1/books/manipulation PUT 
    
    payload example:

        {
            "id": 2,
            "title": "Pomi Dore",
        }

- Returning “No implementation for `GET` method”:

        /v1/books/manipulation GET

- Get all the latest added books limited by some amount with arguments (<limit>)

        /v1/books/latest/<limit> GET 

- Get info(type, name etc …) about a book with arguments (<id>)

        /v1/books/info/<id> GET - 

- Get all ID of books by title with arguments (title)

        /v1/books/ids GET

    payload example:

        {
        "title": "Pomi Dore"
        }