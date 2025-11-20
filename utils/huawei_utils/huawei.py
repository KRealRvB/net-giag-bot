from netmiko import ConnectHandler
from ntc_templates.parse import parse_output
from dotenv import load_dotenv
import os
import logging
from netmiko.exceptions import NetmikoTimeoutException, AuthenticationException, ReadTimeout

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="logs/huawei_connection.log",
    filemode='a'
)

def get_info_huawei(action, host):
    username = os.getenv("LOGIN_HUAWEI")
    password = os.getenv("PASS_HUAWEI")

    device = {
        "device_type": "huawei_telnet",
        "host": host,
        "username": username,
        "password": password,
        "port": 23,
    }
    try:
        with ConnectHandler(**device) as conn:
            conn.send_command("screen-length 0 temporary")
            if action == "int-info":
                return get_if_data_huawei(conn)
            elif action == "vlan-info":
                return get_vlan_data_huawei(conn)
            elif action == "system-info":
                return get_system_data_huawei(conn)
    except ConnectionError as e:
        logging.error(e)
        return None
    except NetmikoTimeoutException as e:
        logging.error(e)
        return None
    except ConnectionRefusedError as e:
        logging.error(e)
        return None
    except AuthenticationException as e:
        logging.error(e)
        return None
    except ReadTimeout as e:
        logging.error(e)
        return None


        

def get_if_data_huawei(conn):
    command = "display interface brief"
    raw_data = conn.send_command(command)
    lines = []
    for if_data in get_parsing_data(command, raw_data):
        lines.append(f"{if_data['interface']}\n  Cтатус: {if_data['phy']}\n  Ошибки:\n    Входящие -> {if_data['inerrors']}\n    Исходящие -> {if_data['outerrors']}\n\n")
    return "".join(lines)


def get_vlan_data_huawei(conn):
    command = "display vlan"
    raw_data = conn.send_command(command)
    lines = []
    for vlan_data in get_parsing_data(command, raw_data):
        lines.append(f"{vlan_data['vlan_id']}\n")
        for interface in vlan_data["interface"]:
            lines.append(f"\t{interface}\n")
    return "".join(lines)


def get_system_data_huawei(conn):
    command = "display version"
    raw_data = conn.send_command(command)
    dict_data = get_parsing_data(command, raw_data)[0]
    return f"Version -> {dict_data['vrp_version']}\nUptime -> {dict_data['uptime']}\n"
    

def get_parsing_data(command, raw_data):
    structured_data = parse_output(
    platform="huawei_vrp",
    command=command,
    data=raw_data
)
    return structured_data
