import socket
import json
import threading 
import time

def print_time_taken(description, start_time):
    end_time = time.time()
    print(f"{description} took {end_time - start_time:.6f} seconds")

def send_init_message(ip, port,iteration_number,neighbors,alpha,iter,nodes):
    message = {
        "init": "INIT",
        "inum": iteration_number,
        "alpha": alpha,
        "iter": iter,
        "neighbors": neighbors,
        "nodes": nodes,
        "num_nodes": num_nodes,
        "sleep_time" : sleep_time
    }
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(json.dumps(message).encode('utf-8'), (ip, port))

def send_messages_to_node(ip, port, neighbors, nodes,iteration_number,alpha,iter):
    send_init_message(ip, port, iteration_number,neighbors,alpha,iter,nodes)

if __name__ == "__main__":
    nodes = [("172.24.180.97", 12345), ("172.24.49.201", 12345),("172.24.93.56", 12345),("172.24.46.85", 12345),("172.24.155.138", 12345)]
    iteration_number = 50
    sleep_time = 0.5
    neighbors = [
        [],
        [2,3,4,5],
        [1],
        [1],
        [1],
        [1]
    ]
    num_nodes = 5
    alpha = 0.1
    iter = 1
    start_time = time.time()
    print(start_time)
    threads = []
    for node in nodes:
        thread = threading.Thread(target=send_messages_to_node, args=(node[0], node[1], neighbors, nodes,iteration_number,alpha,iter))
        threads.append(thread)
        print(thread)
        print_time_taken("Time:",start_time)
    print("------------------------------")
    time.sleep(3)
    
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