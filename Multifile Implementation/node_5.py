import time
import sys
import matplotlib.pyplot as plt
import csv

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

def node_process(node_id, neighbors,x, alpha=0.1, max_iterations=1):
    st = read_state(node_id)
    state = st
    global ii
    for iteration in range(max_iterations):
        new_state = state
        
        # To Receive states from all neighbors
        received_states = []
        for neighbor_id in neighbors:
            neighbor_state = read_state(neighbor_id)
            if neighbor_state is not None:
                received_states.append(neighbor_state)
            else:
                req = 0
                with open(f'log_{neighbor_id}.csv', 'r') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        req = row[1]
                received_states.append(float(req))
        
        if received_states:
            state_update = sum([(neighbor_state - state) for neighbor_state in received_states])
            new_state = state + alpha * state_update
        
        state = new_state
        time.sleep(0.05)
    write_state(node_id,state)
    print(f"Node {node_id} in {x}th iteration: {state}")
    log_state(node_id, ii, state)
    ii+=1

ii = 1

node_id = 5
neighbors = [int(n) for n in sys.argv[1].split(',')]
iteration_number = int(sys.argv[2])
alpha = float(sys.argv[3])
iter = int(sys.argv[4])

for i in range(0,iteration_number):      
    node_process(node_id, neighbors,i+1,alpha,iter)
    time.sleep(1)