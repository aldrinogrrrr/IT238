import socket
import threading

# Server settings
server_ip = "YOUR_SERVER_IP"  # Replace with the actual server IP
server_port = 12345  # Replace with the desired port number

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Register a name with the server
name = input("Enter your name: ")
client_socket.sendto(name.encode('utf-8'), (server_ip, server_port))

def receive_messages():
    while True:
        message, _ = client_socket.recvfrom(1024)
        print(message.decode('utf-8'))

# Start a thread to receive messages
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Send messages to the server and other clients
while True:
    message = input()
    client_socket.sendto(message.encode('utf-8'), (server_ip, server_port))
