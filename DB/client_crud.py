from DB.db_initializer import get_connection
from models.entities import Client


class ClientNotFoundError(Exception):
    pass


async def is_exist_client_by_network(network_id):
    connection = await get_connection()
    async with connection.cursor() as cursor:
        query = "SELECT ClientId FROM Network WHERE Id = %s"
        await cursor.execute(query, (network_id,))
        client_id = await cursor.fetchone()
        if not client_id:
            raise ClientNotFoundError("Client with the specified ID not found.")
        return client_id


async def is_exist_client_by_id(client_id):
    connection = await get_connection()
    async with connection.cursor() as cursor:
        query = "SELECT id FROM Client WHERE Id = %s"
        await cursor.execute(query, (client_id,))
        client_id = await cursor.fetchone()
        if not client_id:
            raise ClientNotFoundError("Client with the specified ID not found.")


async def add_client(client: Client):
    connection = await get_connection()
    async with connection.cursor() as cursor:
        query = "INSERT INTO Client (FirstName, LastName, Email, Phone) VALUES (%s, %s, %s, %s)"
        await cursor.execute(query, (client.FirstName, client.LastName, client.Email, client.Phone))
        await connection.commit()
        return cursor.lastrowid

# hardcode for adding clients
