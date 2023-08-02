import logging
from DB.db_initializer import get_connection
from models.entities import Device


async def add_one_device(device: Device):
    connection = await get_connection()
    async with connection.cursor() as cursor:
        query = "INSERT INTO Device (NetworkID, IP, Mac, Name, Vendor, Info) " \
                "VALUES (%s, %s, %s, %s, %s, %s)"
        await cursor.execute(query, (
            device.NetworkID,
            device.IP,
            device.Mac,
            device.Name,
            device.Vendor,
            device.Info
        ))
        await connection.commit()
        return "added device"


async def update_router(mac):
    connection = await get_connection()
    async with connection.cursor() as cursor:
        query = "UPDATE Device SET IP = %s, Name = %s WHERE Mac = %s"
        await cursor.execute(query, (None, "Router", mac))
        await connection.commit()
        logging.info("router found")
