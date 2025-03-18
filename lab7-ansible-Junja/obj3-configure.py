import os
import time
from netmiko import ConnectHandler
import pandas as pd

#routers

csv_filename = "devices.csv"
try:
    df = pd.read_csv(csv_filename)
    routers = df.to_dict(orient="records")
    #print(routers)
except FileNotFoundError:
    print(f"file  {csv_filename} is not found .")
    routers = []
#routers = [
#    {"device_type": "cisco_ios", "host": "192.168.50.1", "username": "admin", "password": "admin", "router_name": "R1"},
#    {"device_type": "cisco_ios", "host": "192.168.50.2", "username": "admin", "password": "admin", "router_name": "R2"},
#    {"device_type": "cisco_ios", "host": "192.168.50.3", "username": "admin", "password": "admin", "router_name": "R3"},
#]


#check if a router is reachable
def is_reachable(host):
    response = os.system(f"ping -c 2 {host} > /dev/null 2>&1")
    return response == 0  # Returns True if the host is reachable

#through each router
for router in routers:
    print(f"checks router's connection: {router['host']}...")

    if not is_reachable(router['host']):
        print(f"{router['host']} is not available. Next > ")
        continue  

    print(f"{router['host']} is available, deploy configs ")

    try:
        #remove the 'router_name' key before passing to Netmiko
        netmiko_params = {k: v for k, v in router.items() if k != "router_name"}

        
        
        connection = ConnectHandler(**netmiko_params)
        connection.enable()



        #files save them as variable
        config_filename = f"{router['router_name']}.cfg"



        if not os.path.exists(config_filename):
            print(f"CFG file {config_filename} missed. Next to ")
            connection.disconnect()
            continue

        #open and read configs file
        with open(config_filename, "r") as config_file:
            config_lines = config_file.readlines()

        
        
        #send configuration routers
        connection.send_config_set(config_lines)

        #check our configuration
        output = connection.send_command("show ip interface brief")
        print(output)
        connection.disconnect()
        print(f"configs are applied {router['router_name']}. Done {router['router_name']}.")



    except Exception as e:
        print(f"unable to connect to {router['router_name']}: {str(e)}")


