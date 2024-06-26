import socket
import json
import threading 
import time
import os
import subprocess
import csv
import pandas as pd
import matplotlib.pyplot as plt

ns = {
    1: {"ip": "169.254.142.206", "port": 22, "user": "rasp3"},
    2: {"ip": "169.254.71.146", "port": 22, "user": "rasp1"},
}

local_ip = "169.254.253.114"
local_port = 12345

def transfer_and_run(node_id, node_info):
    ip = node_info["ip"]
    port = node_info["port"]
    user = node_info["user"]
    node_script = f"Ns{node_id}.py"
    
    # Transfer node script
    scp_command = f"scp -P {port} {node_script} {user}@{ip}:/home/{user}/Desktop/"
    print(f"Transferring {node_script} to {user}@{ip}...")
    os.system(scp_command)

    # Run node script
    ssh_command = f"ssh -p {port} {user}@{ip} 'python3 /home/{user}/Desktop/{node_script}'"
    print(f"Running {node_script} on {user}@{ip}...")
    subprocess.run(ssh_command, shell=True)


ts = []
for node_id, node_info in ns.items():
    thread = threading.Thread(target=transfer_and_run, args=(node_id, node_info))
    ts.append(thread)
    thread.start()

for thread in ts:
    thread.join()