from scapy.all import *
import mysql.connector

# Loop through the packets and extract device information and connection data
for packet in packets:
    # Extract device information (IP, MAC, Vendor, Info) and connection data (Protocol, Length, Time) from the packet
    # Modify this section according to the structure of your .pcap file and the data you want to extract.

    # Example:
    source_ip = packet['IP'].src
    source_mac = packet['Ether'].src
    destination_ip = packet['IP'].dst
    destination_mac = packet['Ether'].dst
    protocol_id = packet['IP'].proto
    length = len(packet)
    time = str(packet.time)

    # Check if the source device already exists in the Device table, if not, insert it
    # Modify this section based on how you want to identify unique devices.
    cursor.execute("SELECT ID FROM Device WHERE IP = %s AND Mac = %s", (source_ip, source_mac))
    source_device = cursor.fetchone()
    if not source_device:
        insert_device(cursor, network_id=1, ip=source_ip, mac=source_mac, name="Device", vendor="Unknown", info=None)

    # Check if the destination device already exists in the Device table, if not, insert it
    # Modify this section based on how you want to identify unique devices.
    cursor.execute("SELECT ID FROM Device WHERE IP = %s AND Mac = %s", (destination_ip, destination_mac))
    dest_device = cursor.fetchone()
    if not dest_device:
        insert_device(cursor, network_id=1, ip=destination_ip, mac=destination_mac, name="Device", vendor="Unknown", info=None)

    # Insert the connection into the Connection table
    insert_connection(cursor, source_device[0], dest_device[0], protocol_id, length, time)

# Commit the changes and close the database connection
db_conn.commit()
cursor.close()
db_conn.close()
