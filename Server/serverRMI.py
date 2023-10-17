import socket
import threading
import Pyro5.api


serverIp = "192.168.1.35"
serverPort = 12345
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind((serverIp, serverPort))
clientList = {}

print("Server is up and running...")

def broadcast_msg(msg, sender):
    chat_msg = f"{sender}: {msg}"
    for clientAddress in clientList:  # Changed the variable name for clarity
        serverSocket.sendto(chat_msg.encode('utf-8'), clientAddress)

while True:
    clientName, clientAddress = serverSocket.recvfrom(1024)
    clientName = clientName.decode('utf-8')

    if clientAddress not in clientList:
        clientList[clientAddress] = clientName
        print(f"'{clientName}' has joined the chat")
        welcomeMessage = f"{clientName} joined the chat."
        for addr in clientList:
            serverSocket.sendto(welcomeMessage.encode('utf-8'), addr)
    else:
        broadcast_msg(clientName, clientList[clientAddress])




Pyro5.config.SERVERTYPE = "thread"
Pyro5.config.THREADPOOL_SIZE = 20
with Pyro5.api.Proxy("PYRONAME:chatserver") as chat_server:
    client_name = input("Enter your name: ")
    clientSocket.sendto(client_name.encode('utf-8'), (server_ip, server_port))

    def receive_messages():
        while True:
            message, _ = clientSocket.recvfrom(1024)
            print(message.decode('utf-8'))

    def handle_private_chat(target_name):
        while True:
            user_message = input()
            chat_server.send_message(client_name, f"(Private) {target_name}: {user_message}")

    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()

    while True:
        user_message = input()
        if user_message.startswith("/inviteuser"):
            target_name = user_message.split(' ')[1]
            if target_name in chat_server.clientList.values():
                print(f"Inviting {target_name} to a private chat...")
                chat_server.send_invitation(client_name, target_name)
            else:
                print(f"{target_name} is not online or not registered for private chat.")
        else:
            clientSocket.sendto(user_message.encode('utf-8'), (server_ip, server_port))
