import socket
import json

def send_init_message(ip, port,iteration_number,neighbors,alpha,iter,nodes):
    message = {
        "init": "INIT",
        "inum": iteration_number,
        "alpha": alpha,
        "iter": iter,
        "neighbors": neighbors,
        "nodes": nodes,
        "num_nodes": num_nodes,
        "sleep_time": sleep_time
    }
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(json.dumps(message).encode('utf-8'), (ip, port))


if __name__ == "__main__":
    nodes = [("10.194.30.208", 12345), ("10.194.18.177", 12345)]
    iteration_number = 250
    sleep_time = 0.001
    neighbors = [
        [],
        [2],
        [1],
    ]
    num_nodes = 5
    alpha = 0.1
    iter = 1
    for ip, port in nodes:
        send_init_message(ip, port,iteration_number,neighbors,alpha,iter,nodes)

    print("Initialization messages sent to all nodes.")
