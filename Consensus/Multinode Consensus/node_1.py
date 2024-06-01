import socket
import pandas as pd
import time
import json

neighbors=[]
nodes = []
node_id = 1
num_nodes = 1
port_num = 8001

def write_state(node_id, state):
    with open(f'n_{node_id}.txt', 'w') as file:
        file.write(str(state))

def send_state_to_neighbors(ip, port, node_id, state):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        message = f"{node_id},{state}"
        s.sendto(message.encode('utf-8'), (ip, port))

def listen_to_neighbors(s,neighbor_states):
    s.settimeout(1)
    try:
        data, _ = s.recvfrom(1024)
        if data:
            neighbor_id, neighbor_state = data.decode('utf-8').split(',')
            neighbor_states[int(neighbor_id)] = float(neighbor_state)
            print(f"--->Neighbor {neighbor_id} has state value :",neighbor_state)
    except socket.timeout:
        pass


def run_consensus(s,alpha,iter,x):
    state = 0
    neighbor_states = [0]*(num_nodes+1)
    with open(state_file, 'r') as f:
        state = float(f.read().strip())
    for iteration in range(iter):
        # Send state to all neighbors
        for neighbor in neighbors[node_id]:
            ip = nodes[neighbor-1][0]
            port = nodes[neighbor-1][1]
            send_state_to_neighbors(ip, port, node_id, state)

        # Listen to all neighbors
        for neighbor in neighbors[node_id]:
            listen_to_neighbors(s,neighbor_states)
        
        state_update = sum(neighbor_states[neighbor] - state for neighbor in neighbors[node_id])
        state += alpha * state_update
        
        
        pd.DataFrame([[x, state]], columns=["Iteration", "State"]).to_csv(csv_file, mode='a', header=False, index=False)
        print(f"Node {node_id} Iteration {x}: State = {state}")
        # Sleep to synchronize with other nodes
        time.sleep(1)
        write_state(node_id,state)

def clear_csv(file_path):
    with open(file_path, 'w') as file:
        pass

if __name__ == "__main__":
    iterations = 50
    alpha = 0.1
    iter = 1
    clear_csv(f"node{node_id}_state.csv")
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("127.0.0.1", port_num))

        while True:
            data, _ = s.recvfrom(1024)
            if data:
                message = json.loads(data.decode('utf-8'))
                if message.get("init") == "INIT":
                    nodes = message["nodes"]
                    neighbors = message["neighbors"]
                    iterations = message["inum"]
                    iter = message["iter"]
                    alpha = message["alpha"]
                    num_nodes = message["num_nodes"]
                    
                    state_file = f'n_{node_id}.txt'
                    csv_file = f'node{node_id}_state.csv'
                    num_iterations = 50
                    alpha = 0.1  # Step size

                    with open(state_file, 'r') as f:
                        state = float(f.read().strip())
                    
                    for i in range(1,iterations+1):
                        run_consensus(s,alpha,iter,i)
                    break