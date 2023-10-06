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
    client_msg, client_address = server_socket.recvfrom(1024)
    client_msg = client_msg.decode('utf-8')

    if client_address not in client_dict:
        client_dict[client_address] = client_msg
        print(f"'{client_msg}' has joined the chat")
        welcome_msg = f"{client_msg} joined the chat."
        for addr in client_dict:
            server_socket.sendto(welcome_msg.encode('utf-8'), addr)
    else:
        broadcast_msg(client_msg, client_dict[client_address])
