import socket
import threading
import time
import sys


class BanyanBase:
    def __init__(self, process_name):
        self.process_name = process_name


serverIp = "192.168.1.35"
serverPort = 12345
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind((serverIp, serverPort))

clientList = {}
auction_items = {}
auction_end_time = {}

print("Server is up and running...")


def broadcast_msg(msg, sender):
    chat_msg = f"{sender}: {msg}"
    for clientLocation in clientList:
        serverSocket.sendto(chat_msg.encode('utf-8'), clientLocation)


def auction_winner(itemName):
    pass


def check_auction_end_time():
    while True:
        for itemName in list(auction_items.keys()):
            if time.time() > auction_end_time[itemName]:
                auction_winner(itemName)
        time.sleep(1)


def handle_auction_request(clientName, param):
    pass


def handle_bid(clientName, param):
    pass


class AuctionServer(BanyanBase):
    def __init__(self):
        super(AuctionServer, self).__init__(process_name='AuctionServer')
        self.set_subscriber_topic('auction')
        self.udp_thread = threading.Thread(target=self.handle_udp_messages)
        self.udp_thread.start()
        self.timer_thread = threading.Thread(target=check_auction_end_time)
        self.timer_thread.start()

    def handle_udp_messages(self):
        while True:
            data, clientAddress = serverSocket.recvfrom(1024)
            data = data.decode('utf-8')
            data_parts = data.split(':')

            if len(data_parts) >= 3:
                clientName = data_parts[0]
                action = data_parts[1]
                params = data_parts[2:]

                if clientAddress not in clientList:
                    clientList[clientAddress] = clientName
                    print(f"'{clientName}' has joined the auction platform")
                    welcomeMessage = f"{clientName} joined the auction platform."
                    for addr in clientList:
                        serverSocket.sendto(welcomeMessage.encode('utf-8'), addr)

                if action == "Sell":
                    handle_auction_request(clientName, *params)
                elif action == "Bid":
                    handle_bid(clientName, *params)
                elif action == "End":
                    auction_winner(params[0])

    def incoming_message_processing(self, topic, payload):
        clientName = payload['clientName']
        action = payload['action']
        params = payload['params']

        if action == "Sell":
            handle_auction_request(clientName, *params)
        elif action == "Bid":
            handle_bid(clientName, *params)
        elif action == "End":
            auction_winner(params[0])

    def receive_loop(self):
        pass

    def clean_up(self):
        pass

    def set_subscriber_topic(self, param):
        pass


auction_server = AuctionServer()

try:
    auction_server.receive_loop()
except KeyboardInterrupt:
    auction_server.clean_up()
    sys.exit(0)
