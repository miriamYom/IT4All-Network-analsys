import aiomysql
import pymysql


async def connect_db():
    db_server_name = "sql6.freesqldatabase.com"
    db_user = "sql6635076"
    db_password = "IVFgIa9ywj"
    db_name = "sql6635076"
    char_set = "utf8mb4"
    cursor_type = aiomysql.cursors.DictCursor

    connection_object = await aiomysql.connect(host=db_server_name, user=db_user, password=db_password,
                                              db=db_name, charset=char_set, cursorclass=cursor_type)
    # todo: try
    return connection_object
