import socket
import threading

# Server settings
server_ip = "YOUR_SERVER_IP"  # Replace with the actual server IP
server_port = 12345  # Replace with the desired port number

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((server_ip, server_port))

# Store client addresses and their names
client_info = {}

print("Server is running...")

def broadcast(message, sender_name):
    chat_message = f"{sender_name}: {message}"
    for addr in client_info:
        if addr != sender_name:
            server_socket.sendto(chat_message.encode('utf-8'), addr)

while True:
    data, client_address = server_socket.recvfrom(1024)
    data = data.decode('utf-8')

    if client_address not in client_info:
        # Register new client
        client_info[client_address] = data
        print(f"Client '{data}' connected from {client_address}")
        welcome_message = f"Server: Welcome {data}! You can start chatting now."
        server_socket.sendto(welcome_message.encode('utf-8'), client_address)
    else:
        # Broadcast message to all clients
        broadcast(data, client_info[client_address])
