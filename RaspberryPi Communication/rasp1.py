# server.py
import socket

def start_server():
    host = '0.0.0.0'  # Listen on all available interfaces
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print("Server listening on port", port)

        conn, addr = server_socket.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print("Received data:", data.decode())
                conn.sendall(data)  # Echo back the received data

if __name__ == "__main__":
    start_server()
