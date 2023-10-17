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
            chat_client = Pyro5.api.Proxy(f"PYRONAME:chatclient.{addr}")
            chat_client.receive_message(welcome_message.encode('utf-8').decode('utf-8'))
            chat_client.register_user(name, address)

    def send_message(self, sender, message):
        chat_message = f"{sender}: {message}"
        for client_address in self.clientList:
            chat_client = Pyro5.api.Proxy(f"PYRONAME:chatclient.{client_address}")
            chat_client.receive_message(chat_message)

# ... (remaining server code)

# Register the server with Pyro5
server_uri = daemon.register(ChatServer)
ns.register("chatserver", server_uri)

print("Server is up and running...")

# Start the Pyro5 server
daemon.requestLoop()
