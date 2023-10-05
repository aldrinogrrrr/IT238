import socket
import threading

# 14th
def receive_messages(client_socket):
    while True:
        response = client_socket.recv(1024).decode('utf-8')
        if not response:
            break
        print(response)

def send_messages(client_socket):
    while True:
        message = input()
        client_socket.send(message.encode('utf-8'))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = '192.168.1.35'
server_port = 9999

try:
    client.connect((server_ip, server_port))
    print(f"Connected to the server at {server_ip}:{server_port}")

    # Start a thread to continuously receive messages from the server
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    # Start a thread to send messages to the server
    send_thread = threading.Thread(target=send_messages, args=(client,))
    send_thread.start()

    # Wait for both threads to finish
    receive_thread.join()
    send_thread.join()

except ConnectionRefusedError:
    print(f"Connection to {server_ip}:{server_port} was refused. Make sure the server is running.")
except Exception as e:
    print(f"An error occurred: {e}")

finally:
    client.close()
