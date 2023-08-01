from DB.db_initializer import get_connection
from models.entities import Device


# async def add_devices(lst_of_devices):
#     connection = await get_connection()
#     async with connection.cursor() as cursor:
#         query = (
#             '''
#             CREATE TABLE #outputResult (ID int ,Mac varchar(100))
#             INSERT INTO Device(NetworkID, IP, Mac, Name, Vendor, Info)
#             OUTPUT inserted.ID, inserted.Mac
#             INTO #outputResult
#             SELECT dt.NetworkID, dt.IP, dt.Mac, dt.Name, dt.Vendor, dt.Info
#             FROM Device_temp dt LEFT JOIN Device d
#             ON dt.mac = d.mac
#             WHERE d.id IS NULL
#             SELECT * FROM #outputResult
#             '''
#         )
#         cursor.execute(query, lst_of_devices)
#
#         connection.commit()
#         res = await cursor.fetchall()
#         return res


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
        last_identity_id = cursor.lastrowid
        await connection.commit()
        return last_identity_id


async def update_router(mac):
    # Assuming you have a function named 'get_connection' that returns an asynchronous connection object
    connection = await get_connection()

    async with connection.cursor() as cursor:
        query = "UPDATE Device SET IP = %s, Name = %s WHERE Mac = %s"
        await cursor.execute(query, (None,"Router",mac))
        await connection.commit()
