import json
import os

JSON_FILE = "/home/almalinux/ips.json"

HOST = ""

# Load the JSON file
if os.path.exists(JSON_FILE):
    with open(JSON_FILE, "r") as f:
        host_worker_data = json.load(f)
        if host_worker_data:
            # Just take the first host from the list
            HOST = host_worker_data[0]["host"]

broker_url = f'redis://{HOST}:6379/0'
result_backend = f'redis://{HOST}:6379'
timezone = 'Europe/Oslo'

result_backend_transport_options = {
        'retry_policy': {
            'timeout': 5.0 }
}
visibility_timeout = 43200
