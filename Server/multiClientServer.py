import socket
import threading

serverIp = "192.168.1.35"
serverPort = 12345
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind((serverIp, serverPort))
clientList = {}

print("Server is up and running...")


def broadcast_msg(msg, sender):
    chat_msg = f"{sender}: {msg}"
    for clientLocation in clientList:
        serverSocket.sendto(chat_msg.encode('utf-8'), clientLocation)


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
