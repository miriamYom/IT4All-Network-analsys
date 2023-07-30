from typing import Union

from DB.db_initializer import connect_db
from models.entities import Network, Device, UserInDB,Connection

CONNECTION = None


async def get_connection():
    global CONNECTION
    if not CONNECTION:
        CONNECTION = await connect_db()
    return CONNECTION


class ClientNotFoundError(Exception):
    pass


async def is_exist_client(client_id):
    connection = await get_connection()
    with connection.cursor() as cursor:
        query = "SELECT id FROM Client WHERE Id = %s"
        cursor.execute(query, (client_id,))
        result = cursor.fetchone()
        if not result:
            raise ClientNotFoundError("Client with the specified ID not found.")


async def add_user(user: UserInDB):
    connection = await get_connection()
    with connection.cursor() as cursor:
        query_to_check_id = "select id from Role where name = %s"

        cursor.execute(query_to_check_id,())
        query = "INSERT INTO User " \
                "(FirstName,LastName, HashedPassword, RoleID, Email)" \
                " VALUES" \
                "(%s, %s, %s, %s, %s)"
        cursor.execute(query, (user.first_name, user.last_name, user.hashed_password, role_id))
        result = cursor.fetchone()


async def add_network(network: Network):
    connection = await get_connection()
    async with connection.cursor() as cursor:
        query = "INSERT INTO Network (ClientId, LocationName, DateTaken) " \
                "VALUES (%s, %s, %s)"
        await cursor.execute(query, (
            network.client_id,
            network.location_name,
            network.date_taken,
        ))
        last_identity_id = cursor.lastrowid
        await connection.commit()

    return last_identity_id


async def get_network(client_id):
    connection = await get_connection()
    with connection.cursor() as cursor:
        query = "SELECT * FROM Network Where ClientId= %s"
        cursor.execute(query, (client_id,))
        networks = cursor.fetchall()
        return networks


async def get_user(email):
    connection =await get_connection()
    with connection.cursor() as cursor:
        query = "SELECT Password FROM User WHERE email = %s"
        cursor.execute(query, (email,))
        password = cursor.fetchone()
        return password


async def add_devices(lst_of_devices):
    connection = await get_connection()
    with connection.cursor() as cursor:
        query = "INSERT INTO Device(NetworkID,IP,Mac, Name,Vendor,Info) " \
                "Values (%s,%s,%s,%s,%s) "
        cursor.execute(query, lst_of_devices)
        connection.commit()


async def get_networks_devices(network_id: int, mac_address: Union[str, None], vendor: Union[str, None]):
    connection = await get_connection()
    async with connection.cursor() as cursor:
        query = "SELECT * FROM Device WHERE NetworkID = %s"
        params = [network_id]
        if mac_address:
            query += " AND Mac = %s"
            params.append(mac_address)
        if vendor:
            query += " AND Vendor = %s"
            params.append(vendor)
        await cursor.execute(query, params)
        devices = await cursor.fetchall()
    return devices


async def add_connection(connection: Connection):
    connection_to_db = await get_connection()
    with connection_to_db.cursor() as cursor:
        query = "insert into Connection (network_id,ip,mac,name,vendor) Values (%s,%s,%s,%s,%s)"
        cursor.execute(query, ())
        connection_to_db.commit()
