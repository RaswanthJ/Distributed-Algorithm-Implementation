import os
import subprocess

ip = 
port = 22
user = 
node_script = "Add.py"

scp_command = f"scp -P {port} {node_script} {user}@{ip}:/home/{user}/"
print(f"Transferring {node_script} to {user}@{ip}...")
os.system(scp_command)

ssh_command = f"ssh -p {port} {user}@{ip} 'python3 /home/{user}/{node_script}'"
print(f"Running {node_script} on {user}@{ip}...")
subprocess.run(ssh_command, shell=True)