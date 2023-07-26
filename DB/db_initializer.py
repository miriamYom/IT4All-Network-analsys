import pymysql


def connect_db():
    dbServerName = "sql6.freesqldatabase.com"

    dbUser = "sql6635076"

    dbPassword = "IVFgIa9ywj"

    dbName = "sql6635076"

    charSet = "utf8mb4"

    cusrorType = pymysql.cursors.DictCursor

    connectionObject = pymysql.connect(host=dbServerName, user=dbUser, password=dbPassword,

                                       db=dbName, charset=charSet, cursorclass=cusrorType)
    # todo: try
    return connectionObject
