import asyncio
from typing import Union

from DB.db_initializer import get_connection
from models.entities import Network


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
        await connection.commit()
        last_identity_id = cursor.lastrowid

    return last_identity_id


async def get_network(client_id):
    connection = await get_connection()
    with connection.cursor() as cursor:
        query = "SELECT * FROM Network Where ClientId= %s"
        cursor.execute(query, (client_id,))
        networks = cursor.fetchall()
        return networks


class DeviceDoesntExistError(Exception):
    pass


async def get_networks_devices(network_id: Union[int, None], mac_address: Union[str, None], vendor: Union[str, None],
                               client_id: Union[int, None]):
    connection = await get_connection()
    async with connection.cursor() as cursor:
        if client_id:
            query = "SELECT * FROM Device " \
                    "WHERE NetworkId IN " \
                    "(SELECT id FROM Network WHERE ClientId = 1)"
        else:
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
        if not devices:
            raise DeviceDoesntExistError("There are no devices ")
    return devices


async def get_network_details(network_id: int):
    connection = await get_connection()
    async with connection.cursor() as cursor:
        query = """
        SELECT d.*, c.*
        FROM Device d
        JOIN (
            SELECT c1.*
            FROM Connection c1
            JOIN Device dd1 ON c1.DestMac = dd1.Mac
            WHERE dd1.NetworkID = %s
        ) c ON d.Mac = c.SourceMac
        """
        await cursor.execute(query, (network_id,))
        networks_details = cursor.fetchall()
        print("hfvkgiubughigi", networks_details)
        return networks_details


# async def main():
#     network_id = 23
#     await get_network_details(network_id)
#
# # Create the event loop explicitly and run the coroutine function
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())

