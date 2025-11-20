import routeros_api
import os
from dotenv import load_dotenv


def get_if_info_mikrotik(host):
    load_dotenv()
    username = os.getenv("LOGIN")
    password = os.getenv("PASSWORD")
    # try:
    connection = routeros_api.RouterOsApiPool(host=host, username=username, password=password, port=8728, plaintext_login=True)

    api = connection.get_api()
    interfaces = api.get_resource('/interface/ethernet').get()
    message_diag = []
    message_diag.append(f"Interfaces on {host}:\n")
    for iface in interfaces:
        message_diag.append(f" - {iface.get('name')}: {iface.get('running', 'N/A')}\n")
    return "".join(message_diag)
