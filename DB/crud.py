from DB.db_initializer import connect_db
from models.entities import Network

CONNECTION = None


def get_connection():
    global CONNECTION
    if not CONNECTION:
        CONNECTION = connect_db()
    return CONNECTION


class ClientNotFoundError(Exception):
    pass


def is_exist_client(client_id):
    connection = get_connection()

    with connection.cursor() as cursor:
        query = "SELECT id FROM Client WHERE Id = %s"
        cursor.execute(query, (client_id,))
        result = cursor.fetchone()
        if not result:
            raise ClientNotFoundError("Client with the specified ID not found.")


# def add_user(user: User):
#     connection = get_connection()
#     with connection.cursor() as cursor:
#         query = "INSERT INTO User (FirstName, LastName, HashedPassword, RoleID, Email) VALUES (%(first_name)s, %(last_name)s, %(hashe_password)s, %(role_id)s, %(email)s)"
#         cursor.execute(query, (user,))
#         result = cursor.fetchone()


def add_network(network: Network):
    connection = get_connection()
    with connection.cursor() as cursor:
        query = "Insert Into Network (client_id,location_name,date_taken) VALUES (%(client_name)s,%(location_name)s,%(date_taken)s)"
        cursor.execute(query, (network,))
        result = cursor.fetchone()


def get_user(email):
    connection = get_connection()
    with connection.cursor() as cursor:
        query = "SELECT Password FROM User WHERE email = %s"
        cursor.execute(query, (email,))
        password = cursor.fetchone()
        return password


# is_exist_client(11)
# get_user()
