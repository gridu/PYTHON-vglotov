import mysql.connector
import pandas as pd
from mysql.connector import errorcode

DB_NAME = 'employees'

TABLES = {}
TABLES['test_data'] = (
    "CREATE TABLE test_data( date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,"
    " title VARCHAR(500) NOT NULL,"
    " author VARCHAR(500) NOT NULL)")

try:
    cnx = mysql.connector.connect(user='root', password='passw0rd',
                                  host='127.0.0.1')

    cursor = cnx.cursor()


    def create_database(_cursor):
        try:
            _cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)


    try:
        cursor.execute("USE {}".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            print("Database {} created successfully.".format(DB_NAME))
            cnx.database = DB_NAME
        else:
            print(err)
            exit(1)

    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

    add_data = "INSERT INTO test_data (title, author) VALUES ('title', 'author')"

    select_all = "SELECT * FROM test_data"

    cursor.execute(add_data)
    cnx.commit()
    cursor.execute(select_all)
    selected_data = cursor.fetchall()

    query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = 'employees' " \
            "AND TABLE_NAME = 'test_data'"
    cursor.execute(query)
    columns = cursor.fetchall()
    columns = [column[0] for column in columns]
    table_data = pd.DataFrame(selected_data, columns=columns)
    table_data.to_csv('mysql-connector/testCSV.csv', index=True)


except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    cursor.close()
    cnx.close()
