import socket
import threading
import json

serverIp = "192.168.1.35"
serverPort = 12345
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind((serverIp, serverPort))
clientList = {}

print("Server is up and running...")


def broadcast_msg(msg, sender):
    chat_msg = {"type": "chat", "sender": sender, "message": msg}
    for clientLocation in clientList:
        serverSocket.sendto(json.dumps(chat_msg).encode('utf-8'), clientLocation)


def handle_webrtc_offer(client_address, offer, sender):
    offer_msg = {"type": "offer", "sender": sender, "offer": offer}
    serverSocket.sendto(json.dumps(offer_msg).encode('utf-8'), client_address)


def handle_webrtc_answer(client_address, answer, sender):
    answer_msg = {"type": "answer", "sender": sender, "answer": answer}
    serverSocket.sendto(json.dumps(answer_msg).encode('utf-8'), client_address)


def handle_ice_candidate(client_address, candidate, sender):
    candidate_msg = {"type": "ice-candidate", "sender": sender, "candidate": candidate}
    serverSocket.sendto(json.dumps(candidate_msg).encode('utf-8'), client_address)


def handle_client_data(data, client_address):
    if data["type"] == "chat":
        broadcast_msg(data["message"], clientList[client_address])
    elif data["type"] == "offer":
        handle_webrtc_offer(client_address, data["offer"], clientList[client_address])
    elif data["type"] == "answer":
        handle_webrtc_answer(client_address, data["answer"], clientList[client_address])
    elif data["type"] == "ice-candidate":
        handle_ice_candidate(client_address, data["candidate"], clientList[client_address])


def handle_client():
    while True:
        data, client_address = serverSocket.recvfrom(1024)
        data = json.loads(data.decode('utf-8'))

        if client_address not in clientList:
            clientList[client_address] = data["sender"]
            print(f"'{data['sender']}' has joined the chat")
            welcome_message = {"type": "info", "message": f"{data['sender']} joined the chat."}
            for addr in clientList:
                serverSocket.sendto(json.dumps(welcome_message).encode('utf-8'), addr)
        else:
            handle_client_data(data, client_address)


threading.Thread(target=handle_client).start()
