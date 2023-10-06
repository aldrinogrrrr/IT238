import socket
import threading

server_ip = "192.168.1.35"
server_port = 12345
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((server_ip, server_port))

client_info = {}

print("The server is operational...")

def broadcast(message, sender_name):
    chat_message = f"{sender_name}: {message}"
    for addr in client_info:
        if addr != sender_name:
            server_socket.sendto(chat_message.encode('utf-8'), addr)

while True:
    data, client_address = server_socket.recvfrom(1024)
    data = data.decode('utf-8')

    if client_address not in client_info:
        client_info[client_address] = data
        print(f"Client '{data}' is now connected from {client_address}")
        welcome_message = f"Server: Welcome {data}! You can start chatting now."
        server_socket.sendto(welcome_message.encode('utf-8'), client_address)
    else:
        broadcast(data, client_info[client_address])
