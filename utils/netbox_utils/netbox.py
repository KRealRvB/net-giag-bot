import pynetbox
from dotenv import load_dotenv
import os


def get_connection():
    load_dotenv()
    token = os.getenv("TOKEN_NETBOX")
    return pynetbox.api("http://192.168.44.110:8000", token=token)


# def get_ips_loopback_netbox():
#     nb = get_connection()
#     ips = nb.ipam.ip_addresses.filter(role='loopback')
#     ips_loopback = [ip.address[:-3] for ip in ips]
#     return ips_loopback


# def get_ips_crs_netbox():
#     nb = get_connection()
#     ips = nb.ipam.ip_addresses.filter(tag='crs')
#     ips_crs = [ip.address[:-3] for ip in ips]
#     return ips_crs


def get_tag_netbox(requested_ip):
    nb = get_connection()
    ips = list(nb.ipam.ip_addresses.all())
    for ip in ips:
        if requested_ip == ip.address[:-3]:
            return(ip.tags[0]['slug'])
    