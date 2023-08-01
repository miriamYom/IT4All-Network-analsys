import httpx
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


async def analyze_pcap_file(packets, network_id):
    existing_devices = await devices_identification(packets, network_id)
    await connections_identification(packets, existing_devices)


async def get_vendor(mac_address):
    url = f"https://api.macvendors.com/{mac_address}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response.text
        except httpx.HTTPError:
            return None


async def create_device(network_id, ip, mac):
    # Create device and insert it into the DB.
    vendor = await get_vendor(mac)
    device_data = {
        "NetworkID": network_id,
        "IP": str(ip),
        "Mac": mac,
        "Name": "device",
        "Vendor": str(vendor),
        "Info": "---",
    }

    device = Device(**device_data)
    device_id = await add_one_device(device)  # Insert to the DB
    return device_id


async def devices_identification(packets, network_id):
    # a dictionary containing all detected devices.
    # Key: mac address, Value: ID in device table.
    # TODO change to list
    existing_devices = []
    # TODO: add ip null for router
    for packet in packets:
        # Extract the mac address first, if not, it's not a device.
        src_mac = str(packet["Ether"].src)
        dst_mac = str(packet["Ether"].dst)

        # Check if the packet contains the IP layer
        if packet.haslayer(IP):
            # Process source MAC address.
            # TODO:move to out function
            if src_mac not in existing_devices:
                device_id = await create_device(network_id, packet[IP].src, src_mac)
                existing_devices.append(src_mac)
            else:
                pass
            # Process destination MAC address.
            if dst_mac not in existing_devices:
                device_id = await create_device(network_id, packet[IP].dst, dst_mac)
                existing_devices.append(dst_mac)
            else:
                # TODO: (NTH) Check if the IP address is different. If so, it is a router.
                pass

    return existing_devices


async def connections_identification(packets, devices):
    connections = set()
    # TODO: unique by mac adresses
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

