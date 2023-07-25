from scapy.all import *
from io import BytesIO
from scapy.layers.inet import IP


async def open_pcap_file(pcap_file):
    file_content = BytesIO(await pcap_file.read())
    packets = rdpcap(file_content)
    return packets

# def filter_packet(packet):
#     network_range = '192.168.1'
#     return IP in packet and (packet[IP].src.startswith(network_range) or packet[IP].dst.startswith(network_range))


def analyze_pcap_file(packets):
    for packet in packets:
        # if filter_packet(packet):
        if IP in packet:
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            protocol = packet[IP].proto
            pkt_len = len(packet)
            timestamp = packet.time
            print("Source IP:", src_ip)
            print("Destination IP:", dst_ip)
            print("Protocol:", protocol)
            print("Packet Length:", pkt_len)
            print("Timestamp:", timestamp)
            print("=" * 50)
#TODO: Write schemes and insert all the packets. Save as a list and write function in the database that will insert them. goodluck🤩



    print("Packet printing completed.")
