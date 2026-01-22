#!/usr/bin/env python3

import json
import argparse
import sys

IPS_FILE = "ips.json"


def generate_inventory():
    try:
        with open(IPS_FILE, "r") as f:
            data = json.load(f)
    except Exception as e:
        # Ansible requires valid JSON even on failure
        return {
            "_meta": {
                "hostvars": {}
            }
        }

    # Your ips.json format:
    # [
    #   {
    #     "host": "10.x.x.x",
    #     "workers": ["10.x.x.x", ...]
    #   }
    # ]
    inventory_entry = data[0]

    host_ip = inventory_entry["host"]
    worker_ips = inventory_entry["workers"]

    hostvars = {}

    # Host group
    hosts = [host_ip]
    hostvars[host_ip] = {
        "ip": host_ip
    }

    # Workers group
    workers = []
    for ip in worker_ips:
        workers.append(ip)
        hostvars[ip] = {
            "ip": ip
        }

    inventory = {
        "_meta": {
            "hostvars": hostvars
        },
        "all": {
            "children": ["workers"]
        },
        "host": {
            "hosts": hosts
        },
        "workers": {
            "hosts": workers
        }
    }

    return inventory


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--host", action="store")

    args = parser.parse_args()

    if args.list:
        print(json.dumps(generate_inventory(), indent=4))
    elif args.host:
        # Required by Ansible, even if unused
        print(json.dumps({}))
    else:
        print(json.dumps({}))


if __name__ == "__main__":
    main()