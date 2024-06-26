import os

a = 10
b = 20

pth = "/home/rasp3/Desktop/Test/n.txt"

with open(pth,'w') as f:
    f.write(str(a+b))

print("File Created")

ip = "169.254.253.114"
port = 22
user = "rasp2"

n_script = "n.txt"

scp_command = f"scp -P {port} {n_script} {user}@{ip}:/home/{user}/Desktop/Remote Access Test/"
print(f"Transferring {n_script} to {user}@{ip}...")
os.system(scp_command)
