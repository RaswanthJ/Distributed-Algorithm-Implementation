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
    node_script = f"N{node_id}.py"
    
    # Transfer node script
    scp_command = f"scp -P {port} {node_script} {user}@{ip}:/home/{user}/Desktop/"
    print(f"Transferring {node_script} to {user}@{ip}...")
    os.system(scp_command)

    # Run node script
    ssh_command = f"ssh -p {port} {user}@{ip} 'python3 /home/{user}/Desktop/{node_script}'"
    print(f"Running {node_script} on {user}@{ip}...")
    subprocess.run(ssh_command, shell=True)

def print_time_taken(description, start_time):
    end_time = time.time()
    print(f"{description} took {end_time - start_time:.6f} seconds")

def send_init_message(ip, port,iteration_number,neighbors,alpha,iter,nodes,state):
    message = {
        "init": "INIT",
        "inum": iteration_number,
        "alpha": alpha,
        "iter": iter,
        "neighbors": neighbors,
        "nodes": nodes,
        "num_nodes": num_nodes,
        "sleep_time" : sleep_time,
        "state" : state
    }
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(json.dumps(message).encode('utf-8'), (ip, port))

def send_messages_to_node(ip, port, neighbors, nodes,iteration_number,alpha,iter,state):
    send_init_message(ip, port, iteration_number,neighbors,alpha,iter,nodes,state)
    
def data_extractor(fl,d):
    data = []
    with open(f"node{fl}_state.csv", 'r') as file:
        reader = csv.reader(file)
        for row in reader: 
            data.append(float(row[1]))
    d.append(data)


if __name__ == "__main__":
    nodes = [("169.254.142.206",12345), ("169.254.71.146",12345)]
    states = [5,10]
    iteration_number = 100
    sleep_time = 0.01
    neighbors = [
        [],
        [2],
        [1]
    ]
    num_nodes = 2
    alpha = 0.1
    iter = 1
    start_time = time.time()
    print(start_time)
    
    threads = []
    counter = 0
    for node in nodes:
        thread = threading.Thread(target=send_messages_to_node, args=(node[0], node[1], neighbors, nodes,iteration_number,alpha,iter,states[counter]))
        threads.append(thread)
        counter+=1
        print_time_taken("Time:",start_time)
    print("------------------------------")
    time.sleep(1)
    
    print_time_taken("Time:",start_time)
    print("------------------------------")
    for thread in threads:
        print_time_taken(f"Time:{thread}:",start_time)
        thread.start()
    for thread in threads:
        print_time_taken(f"Time:{thread}:",start_time)
        thread.join()
    print("------------------------------")
    print("Initialization messages sent to all nodes.")
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((local_ip,local_port))
        cnt = 0
        while(cnt<num_nodes):
            s.settimeout(sleep_time)
            try:
                data, _ = s.recvfrom(1024)
                if data:
                    node_id, msg = data.decode('utf-8').split(',')
                    if(msg=="done"):
                        cnt+=1
                    
            except socket.timeout:
                pass
    print_time_taken("Time:",start_time)
    d_list = []
    time = []
    for i in range(0,num_nodes):
        data_extractor(i+1,d_list)
    for i in range(1,iteration_number+1):
        time.append(i)
    for i in range(0,num_nodes):
        plt.plot(time,d_list[i], label=f'x{i+1}(t)')
    plt.xlabel('Time')
    plt.ylabel('State')
    plt.title('State Evolution of Nodes')
    plt.legend()
    plt.grid(True)
    plt.show()