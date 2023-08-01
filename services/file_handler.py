from mac_vendor_lookup import MacLookup
from scapy.all import *
from io import BytesIO
from scapy.layers.inet import IP

from DB.crud import add_devices, add_one_device, add_connection
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

    for pct in packets:
        device = {}
        device.network_id = network_id
        device.Name = 'device'
        device.Info = '---'

        if IP in pct:
            device.ip = str(pct[IP].src)

        if "Ether" in pct:
            mac = str(pct["Ether"].src)
            device.Mac = mac
            device.Vendor = 'vendor mvp'  # TODO: order vendor...
            # device['Vendor'] = MacLookup().lookup(mac)

            if mac not in existing_devices.keys():
                connection_id = await add_one_device(**device)  # insert to DB
                existing_devices[mac] = connection_id
                print("device added")

    return existing_devices


async def connections_identification(packets, devices):
    # TODO: filter
    for pct in packets:
        connection = {}

        src_mac = pct["Ether"].src
        connection.Source_id = devices[src_mac]

        dst_mac = pct["Ether"].dst
        connection.Dest_id = devices[dst_mac]

        connection.Protocol_id = 1  # TODO: change it to id of protocol
        connection.Length = len(pct)  # TODO: check if its ok (gpt gave...)
        connection.Time = str(pct.time)

        await add_connection(**connection)
        print("connection added")
