import mysql.connector
import pandas as pd
import logging
from mysql.connector import errorcode

DB_NAME = 'booksDB'

TABLES = {'test_data': (
    "CREATE TABLE test_data( date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,"
    " title VARCHAR(500) NOT NULL,"
    " author VARCHAR(500) NOT NULL)")}

ADD_DATA = "INSERT INTO test_data (title, author) VALUES ('title', 'author')"
SELECT_ALL = "SELECT * FROM test_data"

LOGGER = logging.getLogger()
logging.basicConfig(
    format='[%(asctime)s:%(levelname)s] %(message)s',
    level=logging.DEBUG,
    datefmt='%I:%M:%S')


def create_database(_cursor):
    try:
        _cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        LOGGER.info("Failed creating database: {}".format(err))
        exit(1)


try:
    cnx = mysql.connector.connect(user='root', password='passw0rd',
                                  host='127.0.0.1')
    cursor = cnx.cursor()

    try:
        cursor.execute("USE {}".format(DB_NAME))
    except mysql.connector.Error as err:
        LOGGER.info("Database {} does not exists.".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            LOGGER.info("Database {} created successfully.".format(DB_NAME))
            cnx.database = DB_NAME
        else:
            LOGGER.info(err)
            exit(1)

    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            LOGGER.info("Creating table '{}' ".format(table_name))
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                LOGGER.info("Already exists")
            else:
                LOGGER.info(err.msg)
        else:
            LOGGER.info("OK")

    columns_query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{}' AND TABLE_NAME = " \
                    "'test_data'".format(DB_NAME)

    cursor.execute(ADD_DATA)
    cnx.commit()
    cursor.execute(SELECT_ALL)
    selected_data = cursor.fetchall()
    cursor.execute(columns_query)
    columns = cursor.fetchall()
    columns = [column[0] for column in columns]
    table_data = pd.DataFrame(selected_data, columns=columns)
    table_data.to_csv('mysql-connector/testCSV.csv', index=True)


except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        LOGGER.info("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        LOGGER.info("Database does not exist")
    else:
        LOGGER.info(err)
else:
    cursor.close()
    cnx.close()
