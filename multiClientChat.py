import socket

SERVER_IP = 'your_server_ip'  # Replace with your server's IP address
SERVER_PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    message = input("Enter a message: ")
    if message.lower() == 'q':
        break
    client_socket.sendto(message.encode(), (SERVER_IP, SERVER_PORT))

client_socket.close()
