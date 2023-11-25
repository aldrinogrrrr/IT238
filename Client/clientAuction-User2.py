import socket
import threading
import time

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
    print("Options: SELL <item_name> <starting_bid>, BID <item_name> <bid_amount>, END_AUCTION <item_name>")
    userAction = input("Enter action: ")
    clientSocket.sendto(f"{userName}:{userAction}".encode('utf-8'), (serverIp, serverPort))
    time.sleep(1)  # Adjust this delay as needed for better user interaction
