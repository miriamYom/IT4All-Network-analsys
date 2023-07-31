import asyncio
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


async def add_user(user: UserInDB):
    connection = await get_connection()
    async with connection.cursor() as cursor:
        role_id = await get_role_id(user.RoleName)
        query = "INSERT INTO User (FirstName, LastName, HashedPassword, RoleID, Email) VALUES (%s, %s, %s, %s, %s)"
        await cursor.execute(query, (user.FirstName, user.LastName, user.HashedPassword, role_id, user.Email))
        await connection.commit()
        return cursor.lastrowid


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
    async with connection.cursor() as cursor:
        query = "SELECT * FROM User WHERE email = %s"
        await cursor.execute(query, (email,))
        user = await cursor.fetchone()
    return UserInDB(**user)

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

async def add_devices(lst_of_devices):
    connection = await get_connection()
    async with connection.cursor() as cursor:
        query = (
            '''
            CREATE TABLE #outputResult (ID int ,Mac varchar(100))
            INSERT INTO Device(NetworkID, IP, Mac, Name, Vendor, Info)
            OUTPUT inserted.ID, inserted.Mac 
            INTO #outputResult 
            SELECT dt.NetworkID, dt.IP, dt.Mac, dt.Name, dt.Vendor, dt.Info 
            FROM Device_temp dt LEFT JOIN Device d 
            ON dt.mac = d.mac 
            WHERE d.id IS NULL 
            SELECT * FROM #outputResult
            '''
        )
        cursor.execute(query, lst_of_devices)

        connection.commit()
        res = await cursor.fetchall()
        return res


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


async def add_one_device(device: Device):
    connection = await get_connection()
    async with connection.cursor() as cursor:
        query = "INSERT INTO Device (NetworkID, IP, Mac, Name, Vendor, Info) " \
                "VALUES (%s, %s, %s, %s, %s, %s)"
        await cursor.execute(query, (
            device.network_id,
            device.ip,
            device.Mac,
            device.Name,
            device.Vendor,
            device.Info
        ))
        last_identity_id = cursor.lastrowid
        await connection.commit()
        return last_identity_id

async def add_connections(connections):
    query = "INSERT INTO Device (NetworkID, IP, Mac, Name, Vendor, Info) " \
            "VALUES (%s, %s, %s, %s, %s, %s)"
    try:
        connection = await get_connection()
        async with connection.cursor() as cursor:
            _id = cursor.executemany(query, connections)
            print("last_id", _id)
        connection.commit()
        print("Multiple rows inserted successfully.")
        return True
    except Exception as e:
        connection.rollback()
        print(f"Error: {e}")
        return False









# network_data = {
#     "client_id": 11,
#     "location_name": "Test Location",
#     "date_taken": "25/07/2023",
# }
# network = Network(**network_data)

# asyncio.run(add_network(network))
