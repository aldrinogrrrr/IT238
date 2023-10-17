import socket
import threading
import Pyro5.api

# ... (previous code)
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


# Initialize Pyro5 Server
Pyro5.config.SERVERTYPE = "thread"
Pyro5.config.THREADPOOL_SIZE = 20
daemon = Pyro5.api.Daemon(host="localhost")
ns = Pyro5.api.locate_ns()

# Register the server as a Pyro5 object
@Pyro5.api.expose
class ChatServer:
    def __init__(self):
        self.clientList = {}

    def register_client(self, name, address):
        self.clientList[address] = name
        print(f"'{name}' has joined the chat")
        welcome_message = f"{name} joined the chat."
        for addr in self.clientList:
            chatClient = Pyro5.api.Proxy(f"PYRONAME:chatclient.{addr}")
            chatClient.receive_message(welcome_message.encode('utf-8').decode('utf-8'))
            chatClient.register_user(name, address)

    def send_message(self, sender, message):
        chatMessage = f"{sender}: {message}"
        for client_address in self.clientList:
            chatClient = Pyro5.api.Proxy(f"PYRONAME:chatclient.{client_address}")
            chatClient.receive_message(chatMessage)

# ... (remaining server code)

# Register the server with Pyro5
serverUri = daemon.register(ChatServer)
ns.register("chatserver", serverUri)

print("Server is up and running...")

# Start the Pyro5 server
daemon.requestLoop()
