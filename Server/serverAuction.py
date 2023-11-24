import socket
import threading

serverIp = "192.168.1.35"
serverPort = 12345
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind((serverIp, serverPort))
clientList = {}
auction_items = {}  # Store auction items and their current highest bid

print("Server is up and running...")

def broadcast_msg(msg, sender):
    chat_msg = f"{sender}: {msg}"
    for clientLocation in clientList:
        serverSocket.sendto(chat_msg.encode('utf-8'), clientLocation)

def handle_auction_request(clientName, itemName, starting_bid):
    if itemName not in auction_items:
        auction_items[itemName] = {'highest_bid': starting_bid, 'highest_bidder': clientName}
        broadcast_msg(f"{clientName} added {itemName} for auction.", "Server")
    else:
        serverSocket.sendto(f"Item '{itemName}' already exists for auction.".encode('utf-8'), clientList[clientName])

def handle_bid(clientName, itemName, bid_amount):
    if itemName in auction_items:
        current_bid = auction_items[itemName]['highest_bid']
        if bid_amount > current_bid:
            auction_items[itemName]['highest_bid'] = bid_amount
            auction_items[itemName]['highest_bidder'] = clientName
            broadcast_msg(f"{clientName} placed a bid of {bid_amount} for {itemName}.", "Server")
            serverSocket.sendto(f"You are now the highest bidder for {itemName} with a bid of {bid_amount}.".encode('utf-8'), clientList[clientName])
        else:
            serverSocket.sendto(f"Your bid for {itemName} should be higher than the current highest bid ({current_bid}).".encode('utf-8'), clientList[clientName])
    else:
        serverSocket.sendto(f"No auction exists for '{itemName}'.".encode('utf-8'), clientList[clientName])

def auction_winner(itemName):
    if itemName in auction_items:
        winner = auction_items[itemName]['highest_bidder']
        winning_bid = auction_items[itemName]['highest_bid']
        broadcast_msg(f"The auction for '{itemName}' has ended. Winner: {winner}, Winning bid: {winning_bid}.", "Server")
        del auction_items[itemName]

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

        if action == "SELL":
            handle_auction_request(clientName, *params)

        elif action == "BID":
            handle_bid(clientName, *params)

        elif action == "END_AUCTION":
            auction_winner(params[0])
