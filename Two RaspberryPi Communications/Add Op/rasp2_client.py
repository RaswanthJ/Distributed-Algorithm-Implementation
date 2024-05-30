import socket

def start_client(server_ip):
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((server_ip, port))
        print("Connected to server at", server_ip)
        
        while True:
            num1 = input("Enter the first number: ")
            num2 = input("Enter the second number: ")
            message = f"{num1},{num2}"
            client_socket.sendall(message.encode())
            data = client_socket.recv(1024)
            print("Received result:", data.decode())

if __name__ == "__main__":
    server_ip = '10.194.8.101'   #RaspberryPi Rasp1's IP Address
    start_client(server_ip)
