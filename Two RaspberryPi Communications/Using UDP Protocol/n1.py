import socket

# Configuration
remote_ip = "10.194.18.177"  # Device where data is to be sent 
local_ip = "10.194.30.208"
local_port = 12345
remote_port = 12345

# Create a UDP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)                                                                           
sock.bind((local_ip, local_port))
sock.settimeout(1)  # Set a timeout to avoid blocking indefinitely

def udp_communicate():
    while True:
        # Sending part
        message = input("Enter message to send: ")
        sock.sendto(message.encode(), (remote_ip, remote_port))
        print(f'Sent message to {remote_ip}:{remote_port}')

        # Receiving part
        try:
            data, address = sock.recvfrom(4096)
            print(f'Received message from {address}: {data.decode()}')
        except socket.timeout:
            # Timeout occurred, no data received
            pass

if __name__ == "__main__":
    udp_communicate()