import mysql.connector

# connector.py
dbconfig = {'host': 'ich-db.ccegls0svc9m.eu-central-1.rds.amazonaws.com',
            'user': 'ich1',
            'password': 'password',
            'database': ''
            }

try:
    connection = mysql.connector.connect(**dbconfig)
    cursor = connection.cursor()

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_NO_SUCH_TABLE:
        print("Table does not exist. Please check the table name.")
    else:
        print(err)
finally:
    cursor.close()
    connection.close()