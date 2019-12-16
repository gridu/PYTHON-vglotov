# Library app
Execute next script to start app on default port = 5000 and console logging:
```sh
$ ./run_app.sh
```

Execute this script to start app on custom port <port_number> and logging output option (file or console) by typing 'file' to log into app.logger file and 'console'/nothing to log into console:
```sh
$ ./run_app.sh <port_number> <log_method>
```

This will install all needed requirements and create a database with one table where book entries can be stored using next properties:

    id - assigned automatically
    type - type value is stored in ~enums/BookTypes.py enum
    title - book title
    creation_date - date when book added, user have to specify it
    updated_date_time - time when book title was updated, assigned automatically

### Methods implemented:

- Get list of all books with all 5 attributes mentioned above

        /v1/books GET
        
  expected return code: 200 OK

- Add book with no arguments but request payload as json contains fields (type, title, creation date):
    
        /v1/books/manipulation POST 
    
    payload example:

        {
            "creation_date": "1998-10-11",
            "title": "Pomi Dore",
            "type": "Satire"
        }

   expected return code: 201 CREATED
   
   expected error code: 400 BAD REQUEST

- Delete book with arguments (id)

        /v1/books/manipulation/<id> DELETE
        
   expected return code: 204 NO CONTENT
   
   expected error code: 404 NOT FOUND  

- Change the name of the book with arguments (id)

        /v1/books/manipulation PUT 
    
    payload example:

        {
            "id": 2,
            "title": "Pomi Dore"
        }

   expected return code: 204 NO CONTENT
   
   expected error code: 400 BAD REQUEST
   
- Returning “No implementation for `GET` method”:

        /v1/books/manipulation GET
       
   expected return code: 400 BAD REQUEST

- Get all the latest added books limited by some amount with arguments (limit)

        /v1/books/latest/<limit> GET 
        
   expected return code: 200 OK
   
   expected error code: 404 NOT FOUND

- Get info(type, name etc…) about a book with arguments (id)

        /v1/books/info/<id> GET 
        
   expected return code: 200 OK
   
   expected error code: 404 NOT FOUND
   
- Get all IDs of books by title with arguments

        /v1/books/ids GET
   
    payload example:

        {
            "title": "Pomi Dore"
        }

   expected return code: 200 OK