import socket
import threading

server_ip = "192.168.1.35"
server_port = 12345
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((server_ip, server_port))
client_dict = {}

print("Server is up and running...")

def broadcast_msg(msg, sender):
    chat_msg = f"{sender}: {msg}"
    for client_addr in client_dict:
        server_socket.sendto(chat_msg.encode('utf-8'), client_addr)

while True:
    clientName, clientAddress = server_socket.recvfrom(1024)
    clientName = clientName.decode('utf-8')

    if clientAddress not in client_dict:
        client_dict[clientAddress] = clientName
        print(f"'{clientName}' has joined the chat")
        welcome_msg = f"{clientName} joined the chat."
        for addr in client_dict:
            server_socket.sendto(welcome_msg.encode('utf-8'), addr)
    else:
        broadcast_msg(clientName, client_dict[clientAddress])
