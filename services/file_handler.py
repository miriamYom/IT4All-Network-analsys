from mac_vendor_lookup import MacLookup
from scapy.all import *
from io import BytesIO
from scapy.layers.inet import IP

from DB.crud import add_devices, add_one_device, add_connection, add_connections
from models.entities import Device, Connection


async def open_pcap_file(pcap_file):
    file_content = BytesIO(await pcap_file.read())
    packets = rdpcap(file_content)
    return packets


# def filter_packet(packet):
#     network_range = '192.168.1'
#     return IP in packet and (packet[IP].src.startswith(network_range) or packet[IP].dst.startswith(network_range))


async def analyze_pcap_file(packets, network_id):
    existing_devices = await devices_identification(packets, network_id)
    await connections_identification(packets, existing_devices)



async def devices_identification(packets, network_id):
    # a dictionary containing all detected devices.
    # Key: mac address, Value: ID in device table.
    existing_devices = dict()

    for packet in packets:
        # Extract the mac address first, if not, it's not a device.
        mac = str(packet["Ether"].src)
        if mac not in existing_devices.keys():
            # create device and insert him to DB and to existing_devices.
            device_data = {
                "network_id": network_id,
                "Name": "device",
                "Info": "---",
                "ip": str(packet[IP].src),
                "Mac": mac,
                "Vendor": MacLookup().lookup(mac)
            }

            device = Device(**device_data)
            id = await add_one_device(device)  # insert to DB
            existing_devices[mac] = id
            print("device added")

        else:
            # TODO: (NTH) Check if the IP address is different. If so, it is a router.
            pass

    return existing_devices


async def connections_identification(packets, devices):
    connections = set()

    for packet in packets:
        src_mac = packet["Ether"].src
        dst_mac = packet["Ether"].dst
        connection_data = {
            "Source_id": devices[src_mac],
            "Dest_id": devices[dst_mac],
            "Protocol_id": 1,  # TODO: change it to id of protocol
            "Length": len(packet),
            "Time": str(packet.time),
        }

        connection = Connection(**connection_data)
        connections.add(connection)

    await add_connections(connections)


