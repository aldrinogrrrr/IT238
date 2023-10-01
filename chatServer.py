import socket
import threading


def handle_client(client_socket):
    while True:
        try:

            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break

            print(f"Client User's Message: {data}")

            response = input("Enter your message: ")
            client_socket.send(response.encode('utf-8'))

        except ConnectionResetError:
            print("Client User disconnected")

    client_socket.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 9999))
server.listen(5)

print("Server listening on port 9999")

while True:
    try:
        client_sock, addr = server.accept()
        print(f"Live connection from {addr[0]}:{addr[1]}")

        client_handler = threading.Thread(target=handle_client, args=(client_sock,))
        client_handler.start()
    except KeyboardInterrupt:
        print(f"Terminated by the Server User")

    except Exception as e:
        print(f"Error has occurred: {e}")

server.close()