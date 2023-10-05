import socket
import threading

def receive_messages(client_socket):
    while True:
        response = client_socket.recv(1024).decode('utf-8')
        print(response)

server_ip = '192.168.1.35'
server_port = 9999

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))
    print(f"Connected to the server at {server_ip}:{server_port}")

    # Start a thread to continuously receive messages from the server
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    while True:
        message = input("Enter your message (or ctrl + x to quit): ")
        if message.lower() == 'exit':
            break

        client.send(message.encode('utf-8'))

except ConnectionRefusedError:
    print(f"Connection to {server_ip}:{server_port} was refused. Make sure the server is running.")
except Exception as e:
    print(f"An error occurred: {e}")

finally:
    client.close()
