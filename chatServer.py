import socket
import threading

# 5th version
connected_clients = {}

def handle_client(client_socket, client_address, client_name):
    try:
        print(f"Live connection from {client_address[0]}:{client_address[1]} as {client_name}")

        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break

            print(f"{client_name}: {data}")

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
        client_name = f"Client{len(connected_clients) + 1}"
        connected_clients[client_name] = client_sock

        client_handler = threading.Thread(target=handle_client, args=(client_sock, addr, client_name))
        client_handler.start()
    except KeyboardInterrupt:
        print("Terminated by the Server User")
        break
    except Exception as e:
        print(f"Error has occurred: {e}")

server.close()
