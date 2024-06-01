import socket
import time
import matplotlib.pyplot as plt
import csv

val_list = []

def start_client(server_ip):
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((server_ip, port))
        print("Connected to server at", server_ip)
        start_code = 0
        while(start_code!=1):
            start_code = int(input("Enter 1 to start: "))
        if(start_code==1):
            message = f"{start_code}"
            client_socket.sendall(message.encode())
            for i in range(1,51):
                node_process(1,i,client_socket)

def read_state(node_id):
    try:
        with open(f'n_{node_id}.txt', 'r') as file:
            return float(file.read().strip())
    except FileNotFoundError:
        return None

def write_state(node_id, state):
    with open(f'n_{node_id}.txt', 'w') as file:
        file.write(str(state))

def log_state(node_id, iteration, state):
    with open(f'log_{node_id}.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([iteration, state])
        
def clear_csv(file_path):
    with open(file_path, 'w') as file:
        pass 

def node_process(node_id,x,client_socket,alpha=0.1):
    st = read_state(node_id)
    state = st
    message = f"{state}"
    client_socket.sendall(message.encode())
    data = client_socket.recv(1024)
    print("Received result:", data.decode())
    neighbor_state = float(data.decode())
    state_update = neighbor_state - state
    new_state = state + alpha * state_update        
    state = new_state
    time.sleep(0.01)
    write_state(node_id,state)
    val_list.append(state)
    print(f"Node {node_id} in {x}th iteration: {state}")
    log_state(node_id, x, state)

if __name__ == "__main__":
    clear_csv('log_1.csv')
    server_ip = '127.0.0.1'
    start_client(server_ip)