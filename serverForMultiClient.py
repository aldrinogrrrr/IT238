import socket
import threading

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))


client_addresses = set()

def listen_for_messages():
    while True:
        data, client_address = server_socket.recvfrom(1024)
        print(f"Received message from {client_address}: {data.decode()}")

def broadcast_message():
    while True:
        message = input("Enter a message: ")
        for client_address in client_addresses:
            server_socket.sendto(message.encode(), client_address)

if __name__ == "__main__":
    print(f"Server is listening on {SERVER_HOST}:{SERVER_PORT}")

    message_listener_thread = threading.Thread(target=listen_for_messages)
    message_listener_thread.daemon = True
    message_listener_thread.start()

    broadcast_thread = threading.Thread(target=broadcast_message)
    broadcast_thread.daemon = True
    broadcast_thread.start()

    try:
        while True:
            client_data, client_address = server_socket.recvfrom(1024)
            client_addresses.add(client_address)
    except KeyboardInterrupt:
        print("Server is shutting down.")
        server_socket.close()
