from mac_vendor_lookup import MacLookup
from scapy.all import *
from io import BytesIO
from scapy.layers.inet import IP

from DB.crud import add_devices
from models.entities import Device


async def open_pcap_file(pcap_file):
    file_content = BytesIO(await pcap_file.read())
    packets = rdpcap(file_content)
    return packets

# def filter_packet(packet):
#     network_range = '192.168.1'
#     return IP in packet and (packet[IP].src.startswith(network_range) or packet[IP].dst.startswith(network_range))


async def analyze_pcap_file(packets, network_id):
    # TODO: insert to device table - extract devices - NetworkID, IP, Mac, Name, Vendor, Info
    # TODO: insert to connection table: SourceID (type device), DestID (type device), ProtocolID, Length, Time

    devices = set()
    connections = set()

    my_devices = dict()

    for packet in packets:
        device = Device
        device.network_id = network_id
        device.Name = 'device'
        device.Info = '---'

        if IP in packet:
            device.ip = str(packet[IP].src)

        if "Ether" in packet:
            mac = str(packet["Ether"].src)
            device.Mac = mac
            device.Vendor = 'vendor mvp'
            # device['Vendor'] = MacLookup().lookup(mac)

            devices.add(device)

    await add_devices(devices)

            # connection = {}
            # src_ip = packet[IP].src
            # dst_ip = packet[IP].dst
            # protocol = packet[IP].proto
            # pkt_len = len(packet)
            # timestamp = packet.time
            #
            # connection['SourceID'] = src_ip  # TODO: change it to id of device
            # connection['DestID'] = dst_ip  # TODO: change it to id of device
            # connection['ProtocolID'] = protocol  # TODO: change it to id of protocol
            # connection['Length'] = pkt_len
            # connection['Time'] = timestamp
            #
            # connections.add(connection)
            # TODO: packet_data will be "connection" schema

            # print("Source IP:", src_ip)
            # print("Destination IP:", dst_ip)
            # print("Protocol:", protocol)
            # print("Packet Length:", pkt_len)
            # print("Timestamp:", timestamp)
            # print("=" * 50)
#TODO: Write schemes and insert all the packets. Save as a list and write function in the database that will insert them. goodluck🤩



    print("Packet printing completed.")
