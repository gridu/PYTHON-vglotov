import argparse

import mysql.connector
import logging
import csv
from mysql.connector import errorcode

DB_NAME = 'csvToGetDBdocker'
TABLE_NAME = 'test_data'

TABLES = {TABLE_NAME: (
        "CREATE TABLE " + TABLE_NAME + " ( date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,"
                                       " title VARCHAR(500) NOT NULL,"
                                       " author VARCHAR(500) NOT NULL)")}

ADD_DATA_QUERY = "INSERT INTO {} (title, author) VALUES ('title', 'author')".format(TABLE_NAME)
SELECT_ALL_QUERY = "SELECT * FROM {}".format(TABLE_NAME)

LOGGER = logging.getLogger()
logging.basicConfig(
    format='[%(asctime)s:%(levelname)s] %(message)s',
    level=logging.DEBUG,
    datefmt='%I:%M:%S')


def create_database(_cursor):
    try:
        _cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as _err:
        LOGGER.info("Failed creating database: {}".format(_err))
        exit(1)


def create_tables(_TABLES):
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


def extract_table_data_to_csv(_cursor, path_to_csv, _DB_NAME, _table_name):
    columns_query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{}' AND TABLE_NAME = " \
                    "'{}'".format(_DB_NAME, _table_name)
    _cursor.execute(SELECT_ALL_QUERY)
    selected_data = _cursor.fetchall()
    _cursor.execute(columns_query)
    _columns = _cursor.fetchall()
    _columns = [column[0] for column in _columns]
    fp = open(path_to_csv, 'w')
    myFile = csv.writer(fp)
    myFile.writerow(_columns)
    myFile.writerows(selected_data)
    fp.close()


if __name__ == '__main__':
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

        create_tables(TABLES)
        cursor.execute(ADD_DATA_QUERY)
        cnx.commit()
        extract_table_data_to_csv(cursor, 'mysql-connector/table_data.csv', DB_NAME, TABLE_NAME)

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            LOGGER.info("Something is wrong with your user name or password")
        else:
            LOGGER.info(err)
    else:
        cursor.close()
        cnx.close()
