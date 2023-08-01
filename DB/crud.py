import asyncio
from typing import Union

from DB.db_initializer import connect_db, get_connection
from models.entities import Network, Device, UserInDB, Connection


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





async def get_role_id(role_name: str):
    connection = await get_connection()
    async with connection.cursor() as cursor:
        # Get the RoleID based on the role name
        query_to_check_role_id = "SELECT ID FROM Role WHERE Name = %s"
        await cursor.execute(query_to_check_role_id, (role_name,))
        role_id = await cursor.fetchone()
        # the default is technician
        if not role_id:
            role_id = {'ID':1}
    return role_id





# async def add_devices(lst_of_devices):
#     connection = await get_connection()
#     async with connection.cursor() as cursor:
#         query = "CREATE TABLE #outputResult (ID int ,Mac varchar(100)) " \
#                 "INSERT INTO Device(NetworkID,IP,Mac, Name,Vendor,Info)" \
#                 "OUTPUT inserted.ID,inserted.Mac" \
#                 "INTO #outputResult" \
#                 "SELECT dt.NetworkID,dt.IP,dt.Mac, dt.Name,dt.Vendor,dt.Info" \
#                 "FROM Device_temp dt LEFT JOIN Device d" \
#                 "on dt.mac=d.mac" \
#                 "where d.id is null" \
#                 "SELECT *FROM #outputResult"
#         cursor.execute(query, lst_of_devices)
#
#         connection.commit()
#         res = await cursor.fetchall()
#         return res


async def add_connection(connection: Connection):
    connection_to_db = await get_connection()
    with connection_to_db.cursor() as cursor:
        query = "INSERT INTO Connection (SourceID, DestID, ProtocolID, Length, Time) " \
                "Values (%s, %s, %s, %s, %s)"
        cursor.execute(query, (
            connection.Source_id,
            connection.Dest_id,
            connection.Protocol_id,
            connection.Length,
            connection.Time
        ))
        last_identity_id = cursor.lastrowid
        await connection_to_db.commit()
        return last_identity_id

# network_data = {
#     "client_id": 11,
#     "location_name": "Test Location",
#     "date_taken": "25/07/2023",
# }
# network = Network(**network_data)

# asyncio.run(add_network(network))
