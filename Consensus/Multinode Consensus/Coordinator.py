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
        "num_nodes": num_nodes
    }
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(json.dumps(message).encode('utf-8'), (ip, port))


if __name__ == "__main__":
    nodes = [("127.0.0.1", 8001), ("127.0.0.1", 8002), ("127.0.0.1", 8003),("127.0.0.1", 8004),("127.0.0.1", 8005)]
    iteration_number = 50
    neighbors = [
        [],
        [2,5],
        [1,3],
        [2,4],
        [3,5],
        [1,4]
    ]
    num_nodes = 5
    alpha = 0.1
    iter = 1
    for ip, port in nodes:
        send_init_message(ip, port,iteration_number,neighbors,alpha,iter,nodes)

    print("Initialization messages sent to all nodes.")
