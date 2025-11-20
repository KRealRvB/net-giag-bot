from netmiko import ConnectHandler
from ntc_templates.parse import parse_output
from dotenv import load_dotenv
import os

load_dotenv()

def get_info(action, host):
    username = os.getenv("LOGIN_HUAWEI")
    password = os.getenv("PASS_HUAWEI")

    device = {
        "device_type": "huawei_telnet",
        "host": host,
        "username": username,
        "password": password,
        "port": 23,
    }

    with ConnectHandler(**device) as conn:
        conn.send_command("screen-length 0 temporary")
        if action == "int-info":
            return conn.send_command("display interface brief")
        elif action == "int-vlan":
            return conn.send_command("display vlan")
        elif action == "system-info":
            return conn.send_command("display version")
        

def get_if_data_huawei(action, host):
    command = "display interface brief"
    lines = []
    for if_data in get_parsing_data(action, command):
        lines.append(f"{if_data['interface']}\n  Cтатус: {if_data['phy']}\n  Ошибки:\n    Входящие -> {if_data['inerrors']}\n    Исходящие -> {if_data['outerrors']}\n\n")
    print("".join(lines))
    return "".join(lines)


def get_vlan_data_huawei(action, host):
    command = "display vlan"
    lines = []
    for vlan_data in get_parsing_data(action, command):
        lines.append(f"{vlan_data['vlan_id']}\n")
        for interface in vlan_data["interface"]:
            lines.append(f"\t{interface}\n")
    return "".join(lines)


def get_system_data_huawei(action, host):
    command = "display version"
    dict_data = get_parsing_data(action, command, host)[0]
    return f"Version -> {dict_data['vrp_version']}\nUptime -> {dict_data['uptime']}\n"
    

def get_parsing_data(action, command, host):
    raw_data = get_info(action, host)
    structured_data = parse_output(
    platform="huawei_vrp",
    command=command,
    data=raw_data
)
    return structured_data
    
get_system_data_huawei("system-info")