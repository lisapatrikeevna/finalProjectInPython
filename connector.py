import mysql.connector
from mysql.connector import errorcode
from configs import configRiad,configWrite

# connector.py
class Connector:
    @staticmethod
    def get_db_connection_read():
        try:
            connection = mysql.connector.connect(**configRiad)
            cursor = connection.cursor()
            return connection, cursor
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_NO_SUCH_TABLE:
                print("Table does not exist. Please check the table name.")
            else:
                print(err)
            return None, None


    @staticmethod
    def get_db_connection_write():
        try:
            connection = mysql.connector.connect(**configWrite)
            cursor = connection.cursor()
            return connection, cursor
        except mysql.connector.Error as err:
            print(f"Ошибка подключения к базе данных: {err}")
            return None, None  # Возвращаем None для соединения и курсора


    @staticmethod
    def close_db_connection(connection, cursor):
        if cursor:
            cursor.close()
        if connection:
            connection.close()


