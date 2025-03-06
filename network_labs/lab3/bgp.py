#!/usr/bin/python3
import json
from netmiko import ConnectHandler
import sshInfo  # 引入 sshInfo 模块以加载 sshinfo.json

# 加载 bgp.conf 文件
def load_bgp_config(file_path="bgp.conf"):
    try:
        with open(file_path, "r") as file:
            bgp_config = json.load(file)
            return bgp_config
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: {file_path} is not properly formatted.")
        return None

# 连接到路由器
def connect_to_router(router_name, ssh_info):
    try:
        device = {
            "device_type": "cisco_ios",
            "host": ssh_info["IP"],
            "username": ssh_info["Username"],
            "password": ssh_info["Password"]
        }
        print(f"Connecting to {router_name} ({device['host']})...")
        connection = ConnectHandler(**device)
        print(f"Connected to {router_name} ({device['host']}) successfully!")
        return connection
    except Exception as e:
        print(f"Error: Unable to connect to {router_name} ({ssh_info['IP']}). {str(e)}")
        return None

# 配置 iBGP
def configure_bgp(connection, router_name, bgp_info):
    try:
        commands = [
            f"router bgp {bgp_info['local_asn']}",
            f"neighbor {bgp_info['neighbor_ip']} remote-as {bgp_info['neighbor_remote_as']}",
            f"neighbor {bgp_info['neighbor_ip']} update-source FastEthernet0/0"
        ]
        # 添加需要广播的网络
        for network in bgp_info["NetworkListToAdvertise"]:
            commands.append(f"network {network} mask 255.255.255.255")

        print(f"Configuring BGP on {router_name}...")
        output = connection.send_config_set(commands)
        print(f"BGP configured on {router_name}:\n{output}")
    except Exception as e:
        print(f"Error configuring BGP on {router_name}: {str(e)}")

# 主程序
if __name__ == "__main__":
    # 加载 SSH 和 BGP 配置
    ssh_info = sshInfo.load_ssh_info()  # 使用 sshInfo 模块加载 sshinfo.json
    bgp_config = load_bgp_config()      # 加载 bgp.conf 文件

    if ssh_info and bgp_config:
        print("SSH Info and BGP Configuration loaded successfully!")
        for router_name, bgp_info in bgp_config.items():
            ssh_data = ssh_info.get(router_name)  # 从 sshinfo.json 获取路由器的 SSH 信息
            if ssh_data:
                connection = connect_to_router(router_name, ssh_data)
                if connection:
                    configure_bgp(connection, router_name, bgp_info)
                    connection.disconnect()
                else:
                    print(f"Failed to connect to {router_name}.")
            else:
                print(f"No SSH info found for {router_name} in sshinfo.json.")
    else:
        print("Failed to load SSH Info or BGP Configuration.")
