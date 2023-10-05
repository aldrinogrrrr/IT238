import socket


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = '192.168.1.35'
server_port = 9999


try:
    client.connect((server_ip, server_port))
    print(f"Connected to the server at {server_ip}:{server_port}")

    while True:
        message = input("Enter your message: ")

        client.send(message.encode('utf-8'))

        if message.lower() == 'exit':
            break

        response = client.recv(1024).decode('utf-8')
        print(f"Server's Message: {response}")

except ConnectionRefusedError:
    print(f"Connection to {server_ip}:{server_port} was refused. Make sure the server is running.")
except Exception as e:
    print(f"An error occurred: {e}")

# Close the client socket
client.close()
