import socket
import threading

# Server configuration
SERVER_HOST = '0.0.0.0'  # Listen on all available interfaces
SERVER_PORT = 12345

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))

# Store client addresses
client_addresses = set()

def listen_for_messages():
    while True:
        data, client_address = server_socket.recvfrom(1024)
        print(f"Received message from {client_address}: {data.decode()}")
        # Broadcast the message to all connected clients
        for address in client_addresses:
            if address != client_address:
                server_socket.sendto(data, address)

if __name__ == "__main__":
    print(f"Server is listening on {SERVER_HOST}:{SERVER_PORT}")

    # Start a thread to listen for incoming messages
    message_listener_thread = threading.Thread(target=listen_for_messages)
    message_listener_thread.daemon = True
    message_listener_thread.start()

    try:
        while True:
            client_data, client_address = server_socket.recvfrom(1024)
            client_addresses.add(client_address)
    except KeyboardInterrupt:
        print("Server is shutting down.")
        server_socket.close()
