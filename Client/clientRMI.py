import socket
import threading
import Pyro5.api

server_ip = "localhost"  # Update to the Pyro5 server's IP address
server_port = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# ... (previous code)

# Initialize Pyro5 Client
Pyro5.config.SERVERTYPE = "thread"
Pyro5.config.THREADPOOL_SIZE = 20
with Pyro5.api.Proxy("PYRONAME:chatserver") as chat_server:
    client_name = input("Enter your name: ")
    client_socket.sendto(client_name.encode('utf-8'), (server_ip, server_port))

    def receive_messages():
        while True:
            message, _ = client_socket.recvfrom(1024)
            print(message.decode('utf-8'))

    def handle_private_chat(target_name):
        while True:
            user_message = input()
            chat_server.send_message(client_name, f"(Private) {target_name}: {user_message}")

    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()

    while True:
        user_message = input()
        if user_message.startswith("/invite"):
            target_name = user_message.split(' ')[1]
            if target_name in chat_server.clientList.values():
                private_chat_thread = threading.Thread(target=handle_private_chat, args=(target_name,))
                private_chat_thread.start()
                print(f"Private chat with {target_name} started.")
            else:
                print(f"{target_name} is not online or not registered for private chat.")
        else:
            client_socket.sendto(user_message.encode('utf-8'), (server_ip, server_port))
