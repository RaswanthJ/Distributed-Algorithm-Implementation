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
    2: {"ip": "169.254.71.146", "port": 22, "user": "rasp1"},           #These things are supposed to be changed while adding new nodes
}

local_ip = "169.254.253.114"         #This is Coordinator's ip address
local_port = 12345

def print_time_taken(description, start_time):
    end_time = time.time()
    print(f"{description} took {end_time - start_time:.6f} seconds")
    
def wait_for_done_messages(node_count, port):
    done_count = 0
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(("", port))
        while done_count < node_count:
            data, _ = s.recvfrom(1024)
            message = json.loads(data.decode('utf-8'))
            if message.get("done") == "DONE":
                done_count += 1
                
def send_sync_message(ip, port):
    message = {"sync": "SYNC"}
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((local_ip, local_port))
        s.sendto(json.dumps(message).encode('utf-8'), (ip, port))


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
    num_nodes = 2
    #The above parameters are predetermined
    states = eval(input("Enter the current states of the Nodes as a List:"))
    iteration_number = int(input("Enter the number of iterations that are to be done:"))
    sleep_time = float(input("Enter the sleeptime for each Iteration:"))
    alpha = float(input("Enter Alpha (The parameter that brings the fraction of change in every iteration):"))
    iter = int(input("Enter the number of iterations of correction is done per iteration:"))
    neighbors = eval(input('''Enter the neighbors in an adjacency list format. For example
                           [
                            [],
                            [3],
                            [3],
                            [1,2]
                            ]
                            This is a adjacency list that has three nodes where the edges are between 1,3 and 1,2
                           '''))
    type_of_consensus = str(input("Enter the type of consensus to be handled (Sleep time/Coordinator Synced).For Sleep time type st else type cs:"))
    
    if(type_of_consensus=="st"):
        subprocess.run(["python", "home/rasp2/Desktop/Single RaspberryPi Control/sender.py"])
        threads = []
        counter = 0
        for node in nodes:
            thread = threading.Thread(target=send_messages_to_node, args=(node[0], node[1], neighbors, nodes,iteration_number,alpha,iter,states[counter]))
            threads.append(thread)
            counter+=1
        time.sleep(2)
        
        for thread in threads:
            thread.start()
        for thread in threads:
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
    elif(type_of_consensus=="cs"):
        subprocess.run(["python", "home/rasp2/Desktop/Single RaspberryPi Control/no_sleeptime_sender.py"])
        #To be filled ---------------------------------------------------
        threads = []
        counter = 0
        for node in nodes:
            thread = threading.Thread(target=send_messages_to_node, args=(node[0], node[1], neighbors, nodes,iteration_number,alpha,iter,states[counter]))
            threads.append(thread)
            counter+=1
        
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        print("------------------------------")
        print("Initialization messages sent to all nodes.")
        
        for _ in range(iteration_number):  # Assume 1000 iterations
            # Wait for "done" messages from all nodes
            wait_for_done_messages(len(nodes), local_port)
            print("All nodes completed iteration, sending next sync message.")
            
            for ip, port in nodes:
                send_sync_message(ip, port)
        
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
    else:
        print("INVALID INPUT. TERMINATED")
        os.exit()
    
    
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