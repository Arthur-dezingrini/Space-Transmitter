import threading, socket, rsa
from functions import *

FileExist("ServerKeys")
FileExist("ServerSignature")
FileExist("ServerData")

HOST_A = "127.0.0.1"
PORT_A = 443

server_socket_a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket_a.bind((HOST_A, PORT_A))
server_socket_a.listen()

client_socket_a, client_address_a = server_socket_a.accept()

def receive_messages(client_socket):
    file_name = client_socket.recv(1024).decode()
    file_content = client_socket.recv(1024)
    return file_name, file_content


fileName, fileContent = receive_messages(client_socket_a)
with open(fileName, "wb") as file:
    file.write(fileContent)



receive_thread = threading.Thread(target=receive_messages, args=(client_socket_a, ))