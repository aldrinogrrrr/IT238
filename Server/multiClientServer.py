import socket
import threading

#updated
server_ip = "192.168.1.35"
server_port = 12345
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((server_ip, server_port))
client_info = {}

print("The server is operational...")

def broadcast(message, sender_name):
    chat_message = f"{sender_name}: {message}"
    for addr in client_info:
        server_socket.sendto(chat_message.encode('utf-8'), addr)

while True:
    data, client_address = server_socket.recvfrom(1024)
    data = data.decode('utf-8')

    if client_address not in client_info:
        client_name = data

        welcome_message = f"Server: Welcome {client_name}."
        server_socket.sendto(welcome_message.encode('utf-8'), client_address)

        client_info[client_address] = client_name
        print(f"'{client_name}' is now connected from {client_address}")
    else:
        broadcast(data, client_info[client_address])
