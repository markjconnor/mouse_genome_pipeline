#!/usr/bin/env python3

import json
import subprocess
import argparse

def run(command):
    return subprocess.run(command, capture_output=True, encoding='UTF-8')

def generate_inventory():
    command = "terraform output --json host_ips".split()
    host_ip_data = json.loads(run(command).stdout)

    command = "terraform output --json worker_ips".split()
    worker_ip_data = json.loads(run(command).stdout)
    
    ip_data = host_ip_data + worker_ip_data

    host_vars = {}


    # Host group
    hosts = []
    for ip in host_ip_data:
        hosts.append(ip)
        host_vars[ip] = {"ip": [ip]}

    # Workers group
    workers = []
    for ip in worker_ip_data:
        workers.append(ip)
        host_vars[ip] = {"ip": [ip]}

    
    host_worker_list = [
        {"host": host_ip, "workers": worker_ip_data}
        for host_ip in host_ip_data
    ]

    # Save this mapping to a file
    with open("ips.json", "w") as f:
        json.dump(host_worker_list, f, indent=4)

    '''
    counter = 0
    workers = []

    for a in ip_data:
        name = a
        host_vars[name] = { "ip": [a] }
        workers.append(name)
        counter += 1
    '''
    _meta = {}
    _meta["hostvars"] = host_vars
    _all = { "children": ["workers"] }

    _host = {"hosts": hosts}
    _workers = { "hosts": workers }

    _jd = {}
    _jd["_meta"] = _meta
    _jd["all"] = _all
    _jd["workers"] = _workers
    _jd["host"] = _host


    jd = json.dumps(_jd, indent=4)
    return jd


if __name__ == "__main__":

    ap = argparse.ArgumentParser(
        description = "Generate an inventory from Terraform.",
        prog = __file__
    )

    mo = ap.add_mutually_exclusive_group()
    mo.add_argument("--list",action="store", nargs="*", default="dummy", help="Show JSON of all managed hosts")
    mo.add_argument("--host",action="store", help="Display vars related to the host")

    args = ap.parse_args()

    if args.host:
        print(json.dumps({}))
    elif len(args.list) >= 0:
        jd = generate_inventory()
        print(jd)
    else:
        raise ValueError("Expecting either --host $HOSTNAME or --list")

    
