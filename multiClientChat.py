import socket

# Server configuration
SERVER_IP = 'your_server_ip'  # Replace with your server's IP address
SERVER_PORT = 12345

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    message = input("Enter a message to send (or 'q' to quit): ")
    if message.lower() == 'q':
        break

    client_socket.sendto(message.encode(), (SERVER_IP, SERVER_PORT))

# Close the socket when done
client_socket.close()
