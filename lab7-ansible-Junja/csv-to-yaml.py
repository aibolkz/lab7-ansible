#!/usr/bin/env python3

import csv
import yaml


CSV_FILE = "main.csv"
OUTPUT_YAML = "roles/router/vars/main.yml"

def main():
    routers_dict = {}

    with open(CSV_FILE) as f:
        reader = csv.DictReader(f)
        for row in reader:
            hostname = row['hostname']
            if hostname not in routers_dict:
                routers_dict[hostname] = {
                    'hostname': hostname,
                    'interfaces': []
                }
            ip_addr = row['ip_addr']
            netmask = row['netmask']
            
            intf_data = {
                'interface_type': row['interface_type'],
                'interface_name': row['interface_name'],
                'ip_addr': ip_addr,
                'netmask': netmask,
                'ospf_enabled': row['ospf_enabled'],
                'ospf_pid': row['ospf_pid'],
                'ospf_area': row['ospf_area']
            }
            routers_dict[hostname]['interfaces'].append(intf_data)

    #making dictionary to the list
    final_list = list(routers_dict.values())

    with open(OUTPUT_YAML, 'w') as outf:
        yaml.dump({'routers': final_list}, outf, default_flow_style=False)

if __name__ == "__main__":
    main()
