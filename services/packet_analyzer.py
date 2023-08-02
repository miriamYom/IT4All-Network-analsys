from smtplib import SMTP
import httpx
from scapy.contrib.bgp import BGP
from scapy.layers.dns import DNS
from scapy.layers.http import HTTP
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.l2 import ARP
from scapy.layers.snmp import SNMP
from DB.connection_crud import add_connections, get_protocol_id
from DB.device_crud import add_one_device, update_router
from models.entities import Device, Connection

import logging

# Set the root logger level to "INFO"
logging.basicConfig(level=logging.INFO)


async def analyze_pcap_file(packets, network_id):
    try:
        # Identify devices
        existing_devices = await devices_identification(packets, network_id)
        # Analyze connections
        await connections_identification(packets)
    except Exception as e:
        logging.error(f"Error analyzing pcap file: {e}")


async def get_vendor(mac_address):
    url = f"https://api.macvendors.com/{mac_address}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response.text
        except httpx.HTTPError as e:
            logging.error(f"HTTP error while fetching vendor info: {e}")
            return None
        except Exception as e:
            logging.error(f"Error fetching vendor info: {e}")
            return None


async def get_protocol(packet):
    protocol = 'Unknown'

    if packet.haslayer(TCP):
        protocol = packet['TCP'].name
    elif packet.haslayer(UDP):
        protocol = packet['UDP'].name
    elif packet.haslayer(ARP):
        protocol = packet['ARP'].name
    elif packet.haslayer(ICMP):
        protocol = packet['ICMP'].name
    elif packet.haslayer(DNS):
        protocol = packet['DNS'].name
    elif packet.haslayer(HTTP):
        protocol = packet['HTTP'].name
    elif packet.haslayer(SMTP):
        protocol = packet['SMTP'].name
    elif packet.haslayer(BGP):
        protocol = packet['BGP'].name
    elif packet.haslayer(SNMP):
        protocol = packet['SNMP'].name

    return protocol


async def create_device(network_id, mac, ip):
    try:
        logging.info(f"In create_device: MAC={mac}, IP={ip}")
        vendor = await get_vendor(mac)
        device_data = {
            "NetworkID": network_id,
            "IP": ip,
            "Mac": mac,
            "Name": "device",
            "Vendor": str(vendor),
            "Info": "---",
        }
        device = Device(**device_data)
        await add_one_device(device)
        logging.info(f"Device added successfully.")
        return True
    except Exception as e:
        logging.error(f"Error creating device: {e}")
        return False


async def devices_identification(packets, network_id):
    try:
        # Key: mac address, Value: IP in device table.
        existing_devices = dict()
        router_found = False

        for packet in packets:
            if packet.haslayer(IP):
                src_mac = str(packet["Ether"].src)
                dst_mac = str(packet["Ether"].dst)
                src_ip = packet[IP].src
                dst_ip = packet[IP].dst

                if src_mac not in existing_devices:
                    await create_device(network_id, src_mac, src_ip)
                    existing_devices[src_mac] = src_ip
                else:
                    if existing_devices[src_mac] != src_ip:
                        if not router_found:
                            await update_router(src_mac)
                            router_found = True

                # If it's not ARP broadcast
                if dst_mac not in existing_devices:
                    if dst_mac != 'ff:ff:ff:ff:ff:ff':
                        await create_device(network_id, dst_mac, dst_ip)
                        existing_devices[dst_mac] = dst_ip
                else:
                    if existing_devices[dst_mac] != dst_ip:
                        if not router_found:
                            await update_router(dst_mac)
                            router_found = True

        return existing_devices
    except Exception as e:
        logging.error(f"Error identifying devices: {e}")
        return dict()


async def connections_identification(packets):
    try:

        connections = dict()
        protocols = dict()

        for packet in packets:
            protocol = await get_protocol(packet)
            if protocol in protocols:
                protocol_id = protocols[protocol]
            else:
                protocol_id = await get_protocol_id(protocol)
                protocols[protocol] = protocol_id

            src_mac = packet["Ether"].src
            dst_mac = packet["Ether"].dst
            # TODO: handle brodcast ARP ff:ff:ff:ff:ff:ff packets

            # connection_key = (src_mac, dst_mac)
            connection_data = {
                "SourceMac": src_mac,
                "DestMac": dst_mac,
                # "ProtocolID": protocol_id['ID'],
                "Length": len(packet),
                "Time": str(packet.time),
            }

            connection = Connection(**connection_data)
            if connection in connections:
                connections[connection].add(protocol_id['ID'])

            else:
                connections[connection] = set([protocol_id['ID']])

        await add_connections(connections)
    except Exception as e:
        logging.error(f"Error identifying connections: {e}")
