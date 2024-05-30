import numpy as np
import subprocess
import time

def start_node(node_id, neighbors,iteration_number,alpha,iter):
    node_script = f'node_{node_id}.py'
    subprocess.Popen(['python', node_script, ','.join(map(str, neighbors)),str(iteration_number),str(alpha),str(iter)])

def clear_csv(file_path):
    with open(file_path, 'w') as file:
        pass  # Opening in write mode without writing anything truncates the file



if __name__ == "__main__":
    iteration_number = 50
    num_nodes = 5
    alpha = 0.1
    iter = 1
    clear_csv('log_1.csv')
    clear_csv('log_2.csv')
    clear_csv('log_3.csv')
    clear_csv('log_4.csv')
    clear_csv('log_5.csv')

    neighbors_list = [
        [],         #For 1-base indexing
        [2,5],      # Neighbors of node 1
        [1,3],      # Neighbors of node 2
        [2,4],      # Neighbors of node 3
        [3,5],      # Neighbors of node 4
        [1,4]       #Neighbors of node 5
    ]
    #for i in range(50):
    #print(i+1,"th iteration")
    for node_id in range(1, num_nodes + 1):
        start_node(node_id, neighbors_list[node_id],iteration_number,alpha,iter)
