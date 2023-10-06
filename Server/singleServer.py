import socket
import threading


def handle_client(clientSocket):
    while True:
        try:

            data = clientSocket.recv(1024).decode('utf-8')
            if not data:
                break

            print(f"Client's Message: {data}")

            response = input("Enter your message: ")
            clientSocket.send(response.encode('utf-8'))
        except ConnectionResetError:
            print("Client disconnected.")
            break

    clientSocket.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 9999))  
server.listen(5) 

print("Server listening...")


while True:
    try:
        clientSock, addr = server.accept()
        print(f"Accepted connection from {addr[0]}:{addr[1]}")

        clientHandler = threading.Thread(target=handle_client, args=(clientSock,))
        clientHandler.start()
    except KeyboardInterrupt:
        print("Server terminated by the user.")
        break
    except Exception as e:
        print(f"An error occurred: {e}")

server.close()
