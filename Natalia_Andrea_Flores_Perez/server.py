import socket   
import threading
from criptografia import __generate_keys
from criptografia import encrypt_private_key
from criptografia import decrypt_public_key

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))
server.listen()
print(f"Server running on {host}:{port}")

clients = []
usernames = []

def broadcast(message, _client):
    for client in clients:
        if client != _client:
            private, public = __generate_keys()
            encoded = encrypt_private_key(message, public)
            decrypt_public_key(encoded, private)
            client.send(message)

def handle_messages(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message, client)
        except:
            index = clients.index(client)
            username = usernames[index] 
            broadcast(f"ChatBot: {username} disconnected".encode('utf-8'), client)
            clients.remove(client)
            usernames.remove(username)
            client.close()
            break


def receive_connections():
    while True:
        client, address = server.accept()

        client.send("@username".encode("utf-8"))
        username = client.recv(1024).decode('utf-8')

        clients.append(client)
        usernames.append(username)

        print(f"{username} is connected with {str(address)}")
        __private, public = __generate_keys()
        print(f"Public key of the {username} is {public}")

        message = f"ChatBot: {username} joined the chat!".encode("utf-8")
        broadcast(message, client)
        client.send("Connected to server".encode("utf-8"))
        encoded = encrypt_private_key(message, public)
        decrypt_public_key(encoded, __private)

        thread = threading.Thread(target=handle_messages, args=(client,))
        thread.start()

receive_connections()