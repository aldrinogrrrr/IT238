import socket
import threading


server_ip = "192.168.1.35"
server_port = 12345


client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


name = input("Enter your name: ")
client_socket.sendto(name.encode('utf-8'), (server_ip, server_port))

def receive_messages():
    while True:
        message, _ = client_socket.recvfrom(1024)
        print(message.decode('utf-8'))


receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()


while True:
    message = input("Enter your message: ")
    client_socket.sendto(message.encode('utf-8'), (server_ip, server_port))
