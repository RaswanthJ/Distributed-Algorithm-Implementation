# client.py
import socket

def start_client(server_ip):
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((server_ip, port))
        print("Connected to server at", server_ip)
        
        while True:
            message = input("Enter message to send: ")
            client_socket.sendall(message.encode())
            data = client_socket.recv(1024)
            print("Received echo:", data.decode())

if __name__ == "__main__":
    server_ip = '192.168.1.10'  # Replace with the IP address of Raspberry Pi 1
    start_client(server_ip)
