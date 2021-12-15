import socket   
import threading
from criptografia import __generate_keys
from criptografia import encrypt_private_key
from criptografia import decrypt_public_key

username = input("Enter your username: ")

host = '127.0.0.1'
port = 55555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))


def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')

            if message == "@username":
                client.send(username.encode("utf-8"))
            else:
                print(message)
        except:
            print("An error Ocurred")
            client.close
            break

def write_messages():
    __private, public = __generate_keys()
    while True:
        message = f"{username}: {input('')}"
        encoded = encrypt_private_key(message, public)
        decrypt_public_key(encoded, __private)
        client.send(message.encode('utf-8'))

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

write_thread = threading.Thread(target=write_messages)
write_thread.start()