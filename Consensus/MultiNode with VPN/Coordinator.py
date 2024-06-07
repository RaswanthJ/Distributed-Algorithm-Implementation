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
        "sleep_time" : sleep_time
    }
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(json.dumps(message).encode('utf-8'), (ip, port))


if __name__ == "__main__":
    nodes = [("172.25.166.144", 12345),("172.25.138.224", 12345),("172.25.183.238", 12345),("172.25.178.229", 12345)]
    iteration_number = 50
    sleep_time = 0.1
    # neighbors = [
    #     [],
    #     [3,4],
    #     [],
    #     [1,4],
    #     [1,3],
    # ]
    neighbors = [
        [],
        [2,3],
        [1,3],
        [1,2]
    ]
    num_nodes = 3
    alpha = 0.3
    iter = 1
    for ip, port in nodes:
        send_init_message(ip, port,iteration_number,neighbors,alpha,iter,nodes)

    print("Initialization messages sent to all nodes.")
