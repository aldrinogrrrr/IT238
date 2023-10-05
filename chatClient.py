import socket

# Define the server address and port
SERVER_HOST = 'localhost'
SERVER_PORT = 12345

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    message = input("Enter a message to send (or 'q' to quit): ")
    if message.lower() == 'q':
        break
    client_socket.sendto(message.encode(), (SERVER_HOST, SERVER_PORT))

# Close the socket when done
client_socket.close()
