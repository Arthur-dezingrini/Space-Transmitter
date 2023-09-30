import rsa
import socket
import datetime
import threading
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from functions import *

HOST_B = "127.0.0.1"
PORT_B = 443
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST_B, PORT_B))

FileExist("Keys")
FileExist("dados")
FileExist("Assinaturas")
CreateFile("SondaNames.db")

stop_flag = True
def receive_server_message(client_socket):
    while stop_flag:
        message = client_socket.recv(1024).decode()
        if not message:
            break
        print("Servidor diz:", message)
        

message_thread = threading.Thread(target=receive_server_message, args=(client,))
message_thread.start()

while True:
    print("aguarde...")
    time.sleep(3)
    clear()
    print("""        1 - Cadastrar Sonda e Gerar Par de Chaves
        2 - Enviar Chave da Sonda
        3 - Coletar Dados da Sonda
        4 - Gerar Assinatura dos dados Coletados
        5 - Enviar para a terra os dados
        6 - Sair  """)
    while True:
        try:
            option = int(input("Escolha uma opção: "))
            break
        except:
            print("digite uma opcao valida")

    if option == 1:
        clear()
        sondaName = input("Digite o nome da sonda: ")
        with open("SondaNames.db", "a") as file:
            file.write(f"{sondaName}.public.pem\n")

        (pubKey, privKey) = rsa.newkeys(2048)

        with open(f"./Keys/{sondaName}.public.pem", "wb") as key_file:
            key_file.write(pubKey.save_pkcs1("PEM"))

        with open(f"./Keys/{sondaName}.private.pem", "wb") as key_file:
            key_file.write(privKey.save_pkcs1("PEM"))

    elif option == 2:
        clear()
        with open('SondaNames.db', 'r') as file:
            sonda_list = [line.strip() for line in file.readlines()]
        for contador, nameFile in enumerate(sonda_list, start=1):
            print(f"{contador}: {nameFile}")

        try:
            selectKey = int(input("Escolha uma sonda para enviar ao servidor: "))
            selected_sonda = sonda_list[selectKey - 1]
            with open(f"./Keys/{selected_sonda}", "rb") as file:
                file_content = file.read()

            client.send(f"./Serverkeys/{selected_sonda}".encode())
            client.send(file_content)
            

        except ValueError:
            print("Digite uma opção válida")
        except IndexError:
            print("Sonda selecionada não existe")

    elif option == 3:
        clear()
        questions = ["Local: ", "Temperatura: ","Radiacao Alfa: ", "Radiacao Beta: ", "Radiacao Gama: "]
        answer = []

        for question in questions:
            answer.append(input(question))
            clear()

        today = datetime.date.today()
        filePath = f"./dados/{answer[0]}-{today.day}.{today.month}.txt"

        with open(filePath, 'w') as file:
            for question, ans in zip(questions, answer):
                file.write(f"{question}{ans}\n")
    
        key = get_random_bytes(16)
        with open(filePath, 'rb') as file:
            plaintext = file.read()
            cipher = AES.new(key, AES.MODE_EAX)
            cipherMessage, tag = cipher.encrypt_and_digest(plaintext)

    elif option == 4:
        clear()
        fileList = []
        for file in os.listdir("./dados"):
            fileList.append(file)
        for contador, nameFile in enumerate(fileList, start=1):
            print(f"{contador}: {nameFile}")

        selectFile = int(input("escolha qual dado deseja gerar uma assinatura: "))
        pathData = fileList[selectFile - 1]

        privateKey = rsa.PrivateKey.load_pkcs1(openFile(f"./Keys/{pathData.split('-')[0]}.private.pem", "rb"))
        file = openFile(f"./dados/{pathData}", "rb")
        hash_value = rsa.compute_hash(file, "SHA-256")
        signature = rsa.sign(file, privateKey, "SHA-256")

        with open(f"./Assinaturas/signature-{pathData}", "wb")  as s:
            s.write(signature)
            
    elif option == 5:
        fileList = []
        for file in os.listdir("./dados"):
            fileList.append(file)
        for contador, nameFile in enumerate(fileList, start=1):
            print(f"{contador}: {nameFile}")

        select = int(input("escolha: "))
        with open(f"./Assinaturas/signature-{fileList[select - 1]}", "rb") as file:
                file_content_signature = file.read()
        with open(f"./dados/{fileList[select - 1]}", "rb") as file:
                file_content_dados = file.read()
               
        pathServerData = f"./ServerData/{fileList[select - 1]}"
        pathserverSignature =f"./ServerSignature/{fileList[select - 1]}"

        
        client.send(f"./ServerData/{fileList[select - 1]}".encode())
        client.send(file_content_dados)
        
        time.sleep(0.1)

        client.send(f"./ServerSignature/signature-{fileList[select - 1]}".encode())
        client.send(file_content_signature)
        


    elif option == 6:
        clear()
        stop_flag = False
        break
        
        
message_thread.join()
print("Thread de mensagens encerrada. O programa está sendo encerrado.")

