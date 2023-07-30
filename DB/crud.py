from typing import Union

import pymysql
from fastapi import HTTPException

from DB.db_initializer import connect_db
from models import entities
from models.entities import Network, Device

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
#         query = "INSERT INTO User (FirstName,
#         LastName, HashedPassword, RoleID, Email) VALUES
#         (%(first_name)s, %(last_name)s, %(hashed_password)s, %(role_id)s, %(email)s)"
#         cursor.execute(query, (user,))
#         result = cursor.fetchone()


def add_network(network: entities.Network):
    connection = get_connection()
    with connection.cursor() as cursor:
        query = "Insert Into Network (ClientId,LocationName,DateTaken) " \
                "VALUES (%s,%s,%s)"
        cursor.execute(query, (
            network.client_id,
            network.location_name,
            network.date_taken,
        ))
        last_identity_id = cursor.lastrowid
        connection.commit()
        return last_identity_id


def get_network(client_id):
    connection = get_connection()
    with connection.cursor() as cursor:
        query = "SELECT * FROM Network Where ClientId= %s"
        cursor.execute(query, (client_id,))
        networks = cursor.fetchall()
        return networks


def get_user(email):
    connection = get_connection()
    with connection.cursor() as cursor:
        query = "SELECT Password FROM User WHERE email = %s"
        cursor.execute(query, (email,))
        password = cursor.fetchone()
        return password


# def add_device(device: Device):
#     connection = get_connection()
#     with connection.cursor() as cursor:
#         query = "insert into Device (network_id,ip,mac,name,vendor) Values (%s,%s,%s,%s,%s)"
#         cursor.execute(query, (,))

# network_data = {
#     "client_id": 11,
#     "location_name": "Test Location",
#     "date_taken": "2023-07-25",
# }
# network = Network(**network_data)
#
# add_network(network)

async def get_networks_devices(network_id: int, mac_address: Union[str, None], vendor: Union[str, None]):
    connection = get_connection()
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
