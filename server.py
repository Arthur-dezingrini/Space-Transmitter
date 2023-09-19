import threading, os, socket

if os.path.isdir("Serverkeys"):
    pass
else:
    os.mkdir("Serverkeys")

HOST_A = "127.0.0.1"
PORT_A = 443

server_socket_a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket_a.bind((HOST_A, PORT_A))
server_socket_a.listen()

client_socket_a, client_address_a = server_socket_a.accept()

fileName = client_socket_a.recv(1024).decode()
def receive_messages(client_socket):
    with open("./Serverkeys/{}".format(fileName), 'wb') as arquivo:
        while True:
            dados = client_socket.recv(1024)
            if not dados:   
                break
            arquivo.write(dados)
            

receive_thread = threading.Thread(target=receive_messages, args=(client_socket_a, ))
receive_thread.start()