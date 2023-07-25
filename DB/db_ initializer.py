import mysql.connector
from mysql.connectpipor import Error, errorcode, pooling

try:
    connection_pool = pooling.MySQLConnectionPool(pool_name="pynative_pool",
                                                  pool_size=1,
                                                  pool_reset_session=True,
                                                  host='localhost',
                                                  database='IT4All',
                                                  user='root',
                                                  password='root')
    connection_object = connection_pool.get_connection()

    if connection_object.is_connected():
        db_Info = connection_object.get_server_info()
        print("Connected to MySQL database using connection pool ... MySQL Server version on ", db_Info)

        cursor = connection_object.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("Your connected to - ", record)


except Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Error: Access denied. Check your username and password.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Error: Database does not exist.")
    else:
        print("Error:", err)

finally:
    if connection_object.is_connected():
        cursor.close()
        connection_object.close()
        print("MySQL connection is closed")
