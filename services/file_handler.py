from mac_vendor_lookup import MacLookup
from scapy.all import *
from io import BytesIO
from scapy.layers.inet import IP

from DB.connection_crud import add_connections
from DB.device_crud import add_one_device
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


async def create_device(network_id, ip, mac):
    # Create device and insert it into the DB.
    device_data = {
        "NetworkID": network_id,
        "IP": str(ip),
        "Mac": mac,
        "Name": "device",
        # "Vendor": MacLookup().lookup(mac)
        "Info": "---",
    }

    device = Device(**device_data)
    device_id = await add_one_device(device)  # Insert to the DB
    return device_id


async def devices_identification(packets, network_id):
    # a dictionary containing all detected devices.
    # Key: mac address, Value: ID in device table.
    existing_devices = dict()

    for packet in packets:
        # Extract the mac address first, if not, it's not a device.
        src_mac = str(packet["Ether"].src)
        dst_mac = str(packet["Ether"].dst)

        # Check if the packet contains the IP layer
        if packet.haslayer(IP):
            # Process source MAC address.
            if src_mac not in existing_devices:
                device_id = await create_device(network_id, packet[IP].src, src_mac)
                existing_devices[src_mac] = device_id
                print("Device added")

            # Process destination MAC address.
            if dst_mac not in existing_devices:
                device_id = await create_device(network_id, packet[IP].dst, dst_mac)
                existing_devices[dst_mac] = device_id
                print("Device added")
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
            "SourceMac": src_mac,
            "DestMac": dst_mac,
            "ProtocolName": packet.getlayer(0).name,  # TODO: change it to id of protocol
            "Length": len(packet),
            "Time": str(packet.time),
        }

        connection = Connection(**connection_data)
        connections.add(connection)

    await add_connections(connections)
