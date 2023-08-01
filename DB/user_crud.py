import asyncio

from DB.crud import get_role_id
from DB.db_initializer import get_connection
from models.entities import UserInDB, Client


async def add_user(user: UserInDB):
    connection = await get_connection()
    async with connection.cursor() as cursor:
        role_id = await get_role_id(user.RoleName)
        query = "INSERT INTO User (FirstName, LastName, HashedPassword, RoleID, Email) VALUES (%s, %s, %s, %s, %s)"
        await cursor.execute(query, (user.FirstName, user.LastName, user.HashedPassword, role_id['ID'], user.Email))
        await connection.commit()
        return cursor.lastrowid


async def get_user(email):
    connection = await get_connection()
    async with connection.cursor() as cursor:
        query = "SELECT * FROM User WHERE email = %s"
        await cursor.execute(query, (email,))
        user = await cursor.fetchone()
    return UserInDB(**user)


async def technician_authorization(technician_id, client_id):
    connection = await get_connection()
    async with connection.cursor() as cursor:
        query = "SELECT * FROM ClientForUser WHERE UserID = %s AND ClientID = %s"
        await cursor.execute(query, (technician_id, client_id))
        result = await cursor.fetchone()
        if result:
            return True
        else:
            return False


async def add_client(client: Client):
    connection = await get_connection()
    async with connection.cursor() as cursor:
        query = "INSERT INTO Client (FirstName, LastName, Email, Phone) VALUES (%s, %s, %s, %s)"
        await cursor.execute(query, (client.FirstName, client.LastName, client.Email, client.Phone))
        await connection.commit()
        return cursor.lastrowid

# hardcode for adding clients
