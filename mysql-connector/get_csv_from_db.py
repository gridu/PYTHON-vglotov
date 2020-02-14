import argparse
import mysql.connector
import logging
import csv

from mysql.connector import errorcode

LOGGER = logging.getLogger()
logging.basicConfig(
    format='[%(asctime)s:%(levelname)s] %(message)s',
    level=logging.DEBUG,
    datefmt='%I:%M:%S')


def create_database(_cursor):
    try:
        _cursor.execute(
            f'CREATE DATABASE {DB_NAME} DEFAULT CHARACTER SET \'utf8\'')
    except mysql.connector.Error as _err:
        LOGGER.info(f'Failed creating database: {_err}')
        exit(1)


def create_tables(_TABLES):
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            LOGGER.info(f'Creating table \'{table_name}\'')
            cursor.execute(table_description)
        except mysql.connector.Error as _err:
            if _err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                LOGGER.info('Already exists')
            else:
                LOGGER.info(_err.msg)
        else:
            LOGGER.info('Table created')


def extract_table_data_to_csv(_cursor, path_to_csv, _db_name, _table_name):
    columns_query = f'SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = \'{_db_name}\' AND ' \
                    f'TABLE_NAME = \'{_table_name}\' '
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

    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('--db', type=str, default='db_for_csv')
    PARSER.add_argument('--table', type=str, default='table_for_data')
    ARGS = PARSER.parse_args()

    DB_NAME = ARGS.db
    TABLE_NAME = ARGS.table

    TABLES = {TABLE_NAME: (
        f'CREATE TABLE {TABLE_NAME} ( date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,'
        ' title VARCHAR(500) NOT NULL,'
        ' author VARCHAR(500) NOT NULL)')}

    ADD_DATA_QUERY = f'INSERT INTO {TABLE_NAME} (title, author) VALUES (\'title\', \'author\')'
    SELECT_ALL_QUERY = f'SELECT * FROM {TABLE_NAME}'

    try:
        cnx = mysql.connector.connect(user='root', password='passw0rd',
                                      host='127.0.0.1')
        cursor = cnx.cursor()

        try:
            cursor.execute(f'USE {DB_NAME}')
        except mysql.connector.Error as err:
            LOGGER.info(f'Database {DB_NAME} does not exists.')
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                create_database(cursor)
                LOGGER.info(f'Database {DB_NAME} created successfully.')
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
            LOGGER.info('Something is wrong with your user name or password')
        else:
            LOGGER.info(err)
    else:
        cursor.close()
        cnx.close()
