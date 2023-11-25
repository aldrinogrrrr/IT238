import socket
import threading
import time

from python_banyan.banyan_base import BanyanBase

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

# Functions handle_auction_request, handle_bid, auction_winner...


class AuctionServer(BanyanBase):
    def __init__(self):
        super(AuctionServer, self).__init__(process_name='AuctionServer')
        self.set_subscriber_topic('auction')
        self.udp_thread = threading.Thread(target=self.handle_udp_messages)
        self.udp_thread.start()
        self.timer_thread = threading.Thread(target=self.check_auction_end_time)
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
                    print(f"'{clientName}' has joined the auction")
                    welcomeMessage = f"{clientName} joined the auction."
                    for addr in clientList:
                        serverSocket.sendto(welcomeMessage.encode('utf-8'), addr)

                # Handling actions - SELL, BID, END_AUCTION...
                # (Refer to the provided context in the original code for action handling)

    # Function check_auction_end_time...
    # (The function to check auction end times and declare winners as provided in the original context)

    def incoming_message_processing(self, topic, payload):
        clientName = payload['clientName']
        action = payload['action']
        params = payload['params']

        # Handling actions - SELL, BID, END_AUCTION...
        # (Refer to the provided context in the original code for action handling)

auction_server = AuctionServer()

try:
    auction_server.receive_loop()
except KeyboardInterrupt:
    auction_server.clean_up()
    sys.exit(0)
