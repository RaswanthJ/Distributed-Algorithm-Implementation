import socket

# Configuration
local_ip = "127.0.0.1"  # Loopback address for the same device
local_port = 12345
remote_port = 12346

# Create a UDP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((local_ip, local_port))
sock.settimeout(0.01)  # Set a timeout to avoid blocking indefinitely

def udp_communicate():
    while True:
        # Sending part
        message = input("Enter message to send: ")
        sock.sendto(message.encode(), (local_ip, remote_port))
        print(f'Sent message to {local_ip}:{remote_port}')

        # Receiving part
        try:
            data, address = sock.recvfrom(4096)
            print(f'Received message from {address}: {data.decode()}')
        except socket.timeout:
            # Timeout occurred, no data received
            pass

if __name__ == "__main__":
    udp_communicate()
