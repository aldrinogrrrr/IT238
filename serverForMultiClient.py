import socket
import threading

# Server configuration
SERVER_HOST = '0.0.0.0'  # Listen on all available interfaces
SERVER_PORT = 12345

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))

# Store client addresses and names
clients = {}

def listen_for_messages():
    while True:
        data, client_address = server_socket.recvfrom(1024)
        message = data.decode()

        if client_address not in clients:
            # New client, ask for their name
            server_socket.sendto("Please enter your name: ".encode(), client_address)
            name_data, _ = server_socket.recvfrom(1024)
            name = name_data.decode()
            clients[client_address] = name
            print(f"Welcome {name}!")
            broadcast(f"Welcome {name}!", exclude=[client_address])

        else:
            # Existing client, broadcast their message to others
            sender_name = clients[client_address]
            print(f"{sender_name}: {message}")
            broadcast(f"{sender_name}: {message}", exclude=[client_address])

def broadcast(message, exclude=[]):
    for client_address in clients.keys():
        if client_address not in exclude:
            server_socket.sendto(message.encode(), client_address)

if __name__ == "__main__":
    print(f"Server is listening on {SERVER_HOST}:{SERVER_PORT}")

    # Start a thread to listen for incoming messages
    message_listener_thread = threading.Thread(target=listen_for_messages)
    message_listener_thread.daemon = True
    message_listener_thread.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Server is shutting down.")
        server_socket.close()
