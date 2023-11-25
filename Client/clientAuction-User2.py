import socket
import threading
import time
import sys

class BanyanBase:
    def __init__(self, process_name):
        self.process_name = process_name

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

class AuctionClient(BanyanBase):
    def __init__(self, userName):
        super(AuctionClient, self).__init__(process_name=userName)
        self.set_publisher_topic('auction')

    def send_message(self, action, params):
        message = {'clientName': self.process_name, 'action': action, 'params': params}
        self.publish_payload(message, 'auction')

auction_client = AuctionClient(userName)

while True:
    print("Options: SELL <item_name> <starting_bid> <duration>, BID <item_name> <bid_amount>, END_AUCTION <item_name>")
    option = input("Enter your option: ")
    option_parts = option.split()

    if len(option_parts) >= 2:
        action = option_parts[0]
        params = option_parts[1:]

        if action == "SELL" or action == "BID" or action == "END_AUCTION":
            auction_client.send_message(action, params)
        else:
            print("Invalid action. Please try again.")
