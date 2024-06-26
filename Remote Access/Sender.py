import os
import subprocess

ip = "169.254.142.206"
port = 22
user = "rasp3"
node_script = "Add.py"

scp_command = f"scp -P {port} {node_script} {user}@{ip}:/home/{user}/Desktop/Test/"
print(f"Transferring {node_script} to {user}@{ip}...")
os.system(scp_command)

ssh_command = f"ssh -p {port} {user}@{ip} 'python3 /home/{user}/Desktop/Test/{node_script}'"
print(f"Running {node_script} on {user}@{ip}...")
subprocess.run(ssh_command, shell=True)
