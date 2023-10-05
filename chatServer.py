import socket
import threading

# Store all connected clients and their names
connected_clients = {}

def handle_client(client_socket, client_name):
    try:
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break

            print(f"{client_name}'s Message: {data}")

            response = input(f"Enter your message (or ctrl + x to quit): ")

            for name, socket in connected_clients.items():
                if name != client_name:
                    socket.send(f"{client_name}: {response}".encode('utf-8'))


    except ConnectionResetError:
        print(f"{client_name} disconnected")
    finally:
        client_socket.close()
        del connected_clients[client_name]

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 9999))
server.listen(5)

print("Server listening on port 9999")

while True:
    try:
        client_sock, addr = server.accept()
        print(f"Live connection from {addr[0]}:{addr[1]}")

        client_name = input("Enter your name: ")
        connected_clients[client_name] = client_sock

        client_handler = threading.Thread(target=handle_client, args=(client_sock, client_name))
        client_handler.start()
    except KeyboardInterrupt:
        print("Terminated by the Server User")
        break
    except Exception as e:
        print(f"Error has occurred: {e}")

server.close()
