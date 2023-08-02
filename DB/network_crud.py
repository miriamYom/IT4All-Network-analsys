import logging
from typing import Union
from DB.db_initializer import get_connection
from models.entities import Network
from services.network_visualization import draw
logger = logging.getLogger(__name__)


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
        logger.info(f"network {last_identity_id} added")

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
        params = list()
        if client_id:
            query = "SELECT * FROM Device " \
                    "WHERE NetworkId IN " \
                    "(SELECT id FROM Network WHERE ClientId = %s)"
        else:
            query = "SELECT * FROM Device WHERE NetworkID = %s"
        params.append(network_id)
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
        SELECT d.IP as srcIP,d.Name as srcType,d.Vendor as srcVendor ,dd.IP as destIp,dd.Name as dstType,dd.Vendor as destVendor,c.*,p.*
        FROM Device d JOIN Connection c
            on d.Mac=c.SourceMac
        JOIN Device dd
            on c.DestMac=dd.Mac
        JOIN ConnectionProtocol cd
            on c.ID=cd.ConnectionID
        JOIN Protocol p
            on cd.ProtocolID=p.ID
        where d.NetworkID=%s
        """
        await cursor.execute(query, (network_id,))
        networks_details = cursor.fetchall()
        res = networks_details.result()  # TODO: vizu... can't be here
        return res



