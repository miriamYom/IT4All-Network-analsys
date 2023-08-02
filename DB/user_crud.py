import logging

from DB.db_initializer import get_connection
from models.entities import UserInDB


class UnAuthorizedError(Exception):
    pass


async def get_role_id(role_name: str):
    connection = await get_connection()
    async with connection.cursor() as cursor:
        # Get the RoleID based on the role name
        query_to_check_role_id = "SELECT ID FROM Role WHERE Name = %s"
        await cursor.execute(query_to_check_role_id, (role_name,))
        role_id = await cursor.fetchone()
        # the default is technician
        if not role_id:
            role_id = 1
    return role_id


async def add_user_to_db(user: UserInDB):
    connection = await get_connection()
    async with connection.cursor() as cursor:
        role_id = await get_role_id(user.RoleName)
        query = "INSERT INTO User (FirstName, LastName, HashedPassword, RoleID, Email) VALUES (%s, %s, %s, %s, %s)"
        await cursor.execute(query, (user.FirstName, user.LastName, user.HashedPassword, role_id['ID'], user.Email))
        await connection.commit()
        return cursor.lastrowid


async def get_user_from_db(email):
    connection = await get_connection()
    async with connection.cursor() as cursor:
        query = "SELECT * FROM User WHERE email = %s"
        await cursor.execute(query, (email,))
        user = await cursor.fetchone()
    return UserInDB(**user)


async def technician_authorization(technician_id, client_id):
    logging.info("authorize technician")
    connection = await get_connection()
    async with connection.cursor() as cursor:
        query = "SELECT * FROM ClientForUser WHERE UserID = %s AND ClientID = %s"
        await cursor.execute(query, (technician_id, client_id['ClientId']))
        result = await cursor.fetchone()
        if not result:
            logging.error("You Are not Allowed to access to this client")
            raise UnAuthorizedError("You Are not Allowed to access to this client")
