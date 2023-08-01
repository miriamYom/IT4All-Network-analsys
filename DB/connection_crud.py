from DB.db_initializer import get_connection
import aiomysql


# async def add_connections(connections):
#     query = """
#     INSERT INTO Connection (SourceMac, DestMac, ProtocolName, Length, Time)
#     VALUES (%s, %s, %s, %s, %s)
#     """
#     try:
#         connection = await get_connection()
#         async with connection.cursor() as cursor:
#             for connection_data in connections:
#                 await cursor.execute(
#                     query,
#                     (connection_data.SourceMac, connection_data.DestMac, connection_data.ProtocolName,
#                      connection_data.Length, connection_data.Time)
#                 )
#         connection.commit()
#         print("Multiple rows inserted successfully.")
#         return True
#     except Exception as e:
#         print(f"Error: {e}")
#         return False


async def add_connections(connections):
    # TODO:should add all packets
    if not connections:
        return False

    query = """
    INSERT INTO Connection (SourceMac, DestMac, ProtocolName, Length, Time)
    VALUES (%s, %s, %s, %s, %s)
    """
    try:
        connection = await get_connection()
        async with connection.cursor() as cursor:
            first_connection = next(iter(connections))
            await cursor.execute(
                query,
                (first_connection.SourceMac, first_connection.DestMac, first_connection.ProtocolName,
                 first_connection.Length, first_connection.Time)
            )
            await connection.commit()
            print("First connection inserted successfully.")
            return cursor.lastrowid
    except Exception as e:
        print(f"Error: {e}")
        return False
