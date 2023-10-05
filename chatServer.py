import socket
import threading

# 9th
connected_clients = {}

def handle_client(client_socket, client_address, client_name):
    try:
        print(f"Live connection from {client_address[0]}:{client_address[1]} as {client_name}")

        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break

            print(f"{client_name}: {data}")

    except ConnectionResetError:
        print(f"{client_name} disconnected")
    finally:
        client_socket.close()
        del connected_clients[client_name]

def send_to_clients():
    while True:
        message = input("Server: Enter your message (or ctrl + x to quit): ")
        if message.lower() == 'exit':
            break

        for name, socket in connected_clients.items():
            socket.send(f"Server: {message}".encode('utf-8'))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 9999))
server.listen(5)

print("Server listening on port 9999")

while True:
    try:
        client_sock, addr = server.accept()
        client_name = f"Client{len(connected_clients) + 1}"
        connected_clients[
