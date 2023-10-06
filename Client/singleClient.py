import socket


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverIp = '192.168.1.35'
serverPort = 9999


try:
    client.connect((serverIp, serverPort))
    print(f"Connected to the server at {serverIp}:{serverPort}")

    while True:
        userMessage = input("Enter your message: ")

        client.send(userMessage.encode('utf-8'))

        if userMessage.lower() == 'exit':
            break

        response = client.recv(1024).decode('utf-8')
        print(f"Server's Message: {response}")

except ConnectionRefusedError:
    print(f"Connection to {serverIp}:{serverPort} was refused. Make sure the server is running.")
except Exception as e:
    print(f"An error occurred: {e}")


client.close()
