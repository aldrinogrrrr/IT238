import socket
import threading

serverIp = "192.168.1.35"
serverPort = 12345
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

userName = input("Enter your name: ")
clientSocket.sendto(userName.encode('utf-8'), (serverIp, serverPort))


def receiveMessages():
    while True:
        msg, _ = clientSocket.recvfrom(1024)
        print(msg.decode('utf-8'))


thread = threading.Thread(target=receiveMessages)
thread.start()

while True:
    userMessage = input()
    clientSocket.sendto(userMessage.encode('utf-8'), (serverIp, serverPort))
