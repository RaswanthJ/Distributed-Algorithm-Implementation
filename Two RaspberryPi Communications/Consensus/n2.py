import socket
import time
import matplotlib.pyplot as plt
import csv

val_list = []

def start_server():
    host = '0.0.0.0'  
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(5)                     #The argument 5 is the backlog parameter,
        print("Server listening on port", port)     # which specifies the maximum number of queued connections. 
                                                    #If the queue is full, additional clients attempting to connect may be
                                                    # refused or receive an error until the server can accept more connections.
        conn, addr = server_socket.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                print(data.decode(),type(data.decode()))
                if (int(data.decode())==1):
                    print("YES")
                    break
            for i in range(1,51):
                node_process(2,i,conn)
    
    
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

def node_process(node_id,x,conn,alpha=0.1):
    st = read_state(node_id)
    state = st
    message = f"{state}"
    conn.sendall(message.encode())

    data = conn.recv(1024)
    if not data:
        return
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
    clear_csv('log_2.csv')
    start_server()