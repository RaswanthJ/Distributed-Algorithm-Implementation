import socket
import pandas as pd
import time
import json
import matplotlib.pyplot as plt
import os
import paramiko

def send_file(file,ip,user,path):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip,username=user,port=22)

        sftp = ssh.open_sftp()
        remote_path = os.path.join(path,os.path.basename(file))
        sftp.put(file,remote_path)
        sftp.close()
        ssh.close()
        print(f"File {file} successfully sent.")
    except Exception as e:
        print(f"File Transfer Failed due to {e}")

u_st = 0
start_time = 0
neighbors=[]
nodes = []
node_id = 1
num_nodes = 1
port_num = 12345
val_list = []
neighbor_prev_states=[]
sleep_time = 1
local_ip = "169.254.142.206"     #------------------To be changed-----------------------
user_name = "rasp2"
coor_ip = "169.254.253.114"
coor_port = 12345

def print_time_taken(description, start_time):
    end_time = time.time()
    print(f"{description} took {end_time - start_time:.6f} seconds")

def write_state(node_id, state):
    with open(f'n_{node_id}.txt', 'w') as file:
        file.write(str(state))

def send_state_to_neighbors(ip, port, node_id, state):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        message = f"{node_id},{state}"
        s.sendto(message.encode('utf-8'), (ip, port))

def listen_to_neighbors(s,neighbor_states):
    s.settimeout(sleep_time*0.9)
    try:
        data, _ = s.recvfrom(1024)
        if data:
            neighbor_id, neighbor_state = data.decode('utf-8').split(',')
            neighbor_states[int(neighbor_id)] = float(neighbor_state)
            print(f"--->Neighbor {neighbor_id} has state value :",neighbor_state)
            
    except socket.timeout:
        pass



def run_consensus(s,alpha,iter,x):
    global neighbor_prev_states,sleep_time,start_time
    state = 0
    neighbor_states = [-1]*(num_nodes+1)
    validity = [1]*(num_nodes+1)
    with open(state_file, 'r') as f:
        state = float(f.read().strip())
    for iteration in range(iter):
        # Send state to all neighbors
        for neighbor in neighbors[node_id]:
            ip = nodes[neighbor-1][0]
            port = nodes[neighbor-1][1]
            send_state_to_neighbors(ip, port, node_id, state)

        for neighbor in neighbors[node_id]:
            listen_to_neighbors(s,neighbor_states)
        neighbor_prev_states.append(neighbor_states)
        
        for neighbor in neighbors[node_id]:
            if(neighbor_states[neighbor]==-1 and x!=1):
                if(neighbor_prev_states[-2][neighbor]!=-1):
                    print("Prev state used: " ,neighbor_prev_states[-2][neighbor]," of neighbor:",neighbor)
                    neighbor_states[neighbor] = neighbor_prev_states[-2][neighbor]
                else:
                    validity[neighbor]=0
        #state_update = sum( neighbor_states[neighbor] - state for neighbor in neighbors[node_id])
        state_update = 0
        for neighbor in neighbors[node_id]:
            if validity[neighbor]==1:
                state_update += (neighbor_states[neighbor] - state)
        state += alpha * state_update
        
        pd.DataFrame([[x, state]], columns=["Iteration", "State"]).to_csv(csv_file, mode='a', header=False, index=False)
        print(f"Node {node_id} Iteration {x}: State = {state}")
        print_time_taken(f"Iteration {x}:",u_st)
        # Sleep to synchronize with other nodes
        sle = max(0,sleep_time - (time.time()-u_st-sleep_time*(x-1)))
        time.sleep(sle)
        write_state(node_id,state)
        val_list.append(state)

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
        s.bind((local_ip, port_num))

        while True:
            data, _ = s.recvfrom(1024)
            if data:
                message = json.loads(data.decode('utf-8'))
                if message.get("init") == "INIT":
                    print("INITIATED")
                    nodes = message["nodes"]
                    neighbors = message["neighbors"]
                    iterations = message["inum"]
                    iter = message["iter"]
                    alpha = message["alpha"]
                    num_nodes = message["num_nodes"]
                    sleep_time = message["sleep_time"]
                    state_sent = message["state"]
                    
                    state_file = f'n_{node_id}.txt'
                    csv_file = f'node{node_id}_state.csv'
                    num_iterations = 50
                    alpha = 0.1  # Step size

                    write_state(node_id,state_sent)
                    state = state_sent
                    time_list =[0]
                    val_list.append(state_sent)
                    time.sleep(3)
                    u_st = time.time()
                    for i in range(1,iterations+1):
                        run_consensus(s,alpha,iter,i)
                        time_list.append(i)
                        
                    
                    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                        message = f"{node_id},done"
                        s.sendto(message.encode('utf-8'), (coor_ip,coor_port))
                    
                    path = f"/home/{user_name}/Desktop/Single_Pi_Control/"
                    send_file(csv_file,coor_ip,user_name,path)
                    
                    
                    plt.plot(time_list, val_list , label='x(t)')
                    plt.xlabel('Time')
                    plt.ylabel('State')
                    plt.title(f'State Evolution of Node {node_id}')
                    plt.legend()
                    plt.grid(True)
                    plt.show()
                    break
