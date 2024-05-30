import socket
import threading

def handle_client(conn, addr):
    print('Connected by', addr)
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            numbers = data.decode().split(',')
            num1, num2 = int(numbers[0]), int(numbers[1])
            result = num1 + num2
            print(f"Received numbers: {num1} and {num2}, sending result: {result}")
            conn.sendall(str(result).encode())

def start_server():
    host = '0.0.0.0'  
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(5)                     #The argument 5 is the backlog parameter, which specifies the maximum number of queued connections. 
        print("Server listening on port", port)     #If the queue is full, additional clients attempting to connect may be refused or receive an error until the server can accept more connections.

        while True:
            conn, addr = server_socket.accept()
            client_handler = threading.Thread(target=handle_client, args=(conn, addr))     #Threading is done to handle multiple clients at the same time
            client_handler.start()

if __name__ == "__main__":
    start_server()
