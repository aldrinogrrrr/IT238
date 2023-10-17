import socket
import threading
import Pyro5.api

# ... (previous code)

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
