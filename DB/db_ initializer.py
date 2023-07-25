import pymysql

connection = pymysql.connect(
    host="localhost",
    db="IT4All",
    user='root',
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)

if connection.open:
    print("the connection is opened")