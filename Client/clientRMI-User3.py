import socket
import threading
import Pyro5.api


serverIp = "192.168.1.35"
serverPort = 12345
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

userName = input("Enter your name: ")
clientSocket.sendto(userName.encode('utf-8'), (serverIp, serverPort))


Pyro5.config.SERVERTYPE = "thread"
Pyro5.config.THREADPOOL_SIZE = 20
with Pyro5.api.Proxy("PYRONAME:chatserver") as chat_server:
    def receive_messages():
        while True:
            msg, _ = clientSocket.recvfrom(1024)
            print(msg.decode('utf-8'))

    def handle_private_chat(targetName):
        while True:
            userMessage = input()
            chat_server.send_message(userName, f"(Private) {targetName}: {userMessage}")

    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()

    while True:
        userMessage = input()
        if userMessage.startswith("/inviteuser"):
            targetName = userMessage.split(' ')[1]
            if targetName in chat_server.clientList.values():
                private_chat_thread = threading.Thread(target=handle_private_chat, args=(targetName,))
                private_chat_thread.start()
                print(f"Private chat with {targetName} started.")
            else:
                print(f"{targetName} is not online or not registered for private chat.")
        else:
            clientSocket.sendto(userMessage.encode('utf-8'), (serverIp, serverPort))
