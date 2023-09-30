import threading
import socket
import rsa
from functions import *
HOST_A = "127.0.0.1"
PORT_A = 443

server_socket_a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket_a.bind((HOST_A, PORT_A))
server_socket_a.listen()

FileExist("Serverkeys")
FileExist("ServerData")
FileExist("ServerSignature")

files = []

def receive_file(client_socket):
    file_name = client_socket.recv(1024).decode()
    file_content = client_socket.recv(1024)
    with open(file_name, "wb") as file:
        file.write(file_content)
        files.append(file)


def handle_client(client_socket):
    received_files = []
    while True:
        file_name = client_socket.recv(1024).decode()
        file_content = client_socket.recv(1024)

        with open(file_name, "wb") as file:
            file.write(file_content)
        received_files.append(file_name)

        if len(received_files) == 2:
            data_file_name = received_files[0]
            signature_file_name = received_files[1]
            verification_result = verify_signature(data_file_name, signature_file_name)
            if verification_result:
                client_socket.send("O arquivo é confiável.".encode())
            else:
                client_socket.send("O arquivo não é confiável.".encode())

def verify_signature(data_file_name, signature_file_name):
    sonda_name = data_file_name.split('/')[2]
    sonda_name = sonda_name.split("-")[0]

    public_key_file = f"./Serverkeys/{sonda_name}.public.pem"
    with open(public_key_file, "rb") as key_file:
        public_key = rsa.PublicKey.load_pkcs1(key_file.read())


    with open(data_file_name, "rb") as data_file, open(signature_file_name, "rb") as signature_file:
        data_content = data_file.read()
        signature = signature_file.read()

    try:
        rsa.verify(data_content, signature, public_key)
        print("A assinatura é valida. Os dados não foram adulterados.")
        return True
    except rsa.VerificationError:
        print("A assinatura é inválida. Os dados podem ter sido adulterados.")
        return False

client_threads = []

try:
    while True:
        client_socket, client_address = server_socket_a.accept()
        print(f"Conexão recebida de {client_address[0]}:{client_address[1]}")
        
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()
        client_threads.append(client_thread)

except KeyboardInterrupt:
    print("Servidor encerrado.")
    server_socket_a.close()
    for thread in client_threads:
        thread.join()