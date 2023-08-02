import logging

from DB.db_initializer import get_connection


async def get_protocol_id(protocol: str):
    connection = await get_connection()
    async with connection.cursor() as cursor:
        # Get the ProtocolID based on the protocol name
        query_to_check_role_id = "SELECT ID FROM Protocol WHERE Name = %s"
        logging.info(f"Executing query: {query_to_check_role_id} with parameter: {protocol}")
        await cursor.execute(query_to_check_role_id, (protocol,))
        protocol_id = await cursor.fetchone()
        return protocol_id


async def add_connections(connections_dict):
    if not connections_dict:
        return False

    query = """
    INSERT INTO Connection (SourceMac, DestMac, Length, Time)
    VALUES (%s, %s, %s, %s)
    """

    query_connection_protocol = """
    INSERT INTO ConnectionProtocol (ConnectionID, ProtocolID)
    VALUES (%s, %s)
    """

    try:
        connection = await get_connection()
        async with connection.cursor() as cursor:
            for connection_obj, protocol_ids in connections_dict.items():
                try:
                    await cursor.execute(query, (connection_obj.SourceMac, connection_obj.DestMac, connection_obj.Length, connection_obj.Time))
                    connection_id = cursor.lastrowid
                    for protocol_id in protocol_ids:
                        await cursor.execute(query_connection_protocol, (connection_id, protocol_id))
                except Exception as e:
                    # If there's an error, log it and continue to the next connection
                    logging.error(f"Error inserting connection src mac: {connection_obj.SourceMac}, dst mac:{connection_obj.DestMac}")
                    continue
            await connection.commit()
            logging.info(f"{len(connections_dict)} connections inserted successfully.")
            return True
    except Exception as e:
        logging.error(f"Error: {e}")
        return False

