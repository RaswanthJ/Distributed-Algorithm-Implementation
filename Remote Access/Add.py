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

path = f"/home/{user}/Desktop/Remote Access Test/"

send_file(n_script,ip,user,path)
