import socket
import keyboard

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = '192.168.1.35'
server_port = 9999

try:
    client.connect((server_ip, server_port))
    print(f"Connected to the server at {server_ip}:{server_port}")

    client_name = input("Enter your name: ")
    client.send(client_name.encode('utf-8'))

    while True:
        message = input("Enter your message (or ctrl + x to quit): ")
        client.send(message.encode('utf-8'))
        if message.lower() == 'exit':
            break

        response = client.recv(1024).decode('utf-8')
        print(response)

        if keyboard.is_pressed('ctrl') and keyboard.is_pressed('x'):
            break

except ConnectionRefusedError:
    print(f"Connection to {server_ip}:{server_port} was refused. Make sure the server is running.")
except Exception as e:
    print(f"An error occurred: {e}")

client.close()
