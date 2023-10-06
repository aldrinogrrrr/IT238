import socket
import threading

server_ip = "192.168.1.35"
server_port = 12345
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

user_name = input("Enter your name: ")
client_socket.sendto(user_name.encode('utf-8'), (server_ip, server_port))

def receive_messages():
    while True:
        msg, _ = client_socket.recvfrom(1024)
        print(msg.decode('utf-8'))

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

while True:
    user_msg = input()
    client_socket.sendto(user_msg.encode('utf-8'), (server_ip, server_port))
