import rsa
import socket
import subprocess
import datetime
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from functions import *

#subprocess.Popen("python server.py", shell=True, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

HOST_B = "127.0.0.1"
PORT_B = 443
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST_B, PORT_B))

while True:
    clear()
    print("""1 - Cadastrar Sonda e Gerar Par de Chaves
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
        FileExist("keys")
        sondaName = input("Digite o nome da sonda: ")
        (pubKey, privKey) = rsa.newkeys(2048)

        with open("./keys/{}.public.pem".format(sondaName), "wb") as key_file:
            key_file.write(pubKey.save_pkcs1("PEM"))

        with open("./keys/{}.private.pem".format(sondaName), "wb") as key_file:
            key_file.write(privKey.save_pkcs1("PEM"))

    elif option == 2:
        clear()
        FileName = input("digite o nome da sonda que deseja enviar a chave publica: ")
        client.send("./keys/{}.public.pem".format(FileName).encode())
        with open("./keys/{}.public.pem".format(FileName), "rb") as file:
            while True:
                dados = file.read(2048)
                if not dados:
                    break
                client.send(dados)

    elif option == 3:
        clear()
        FileExist("dados")
        questions = ["Local: ", "Temperatura: ",
                     "Radiação Alfa: ", "Radiação Beta: ", "Radiação Gama: "]
        answer = []

        for question in questions:
            answer.append(input(question))
            clear()
        filePath = "./dados/{}{}-{}".format(
            answer[0], datetime.date.today().day, datetime.date.today().month)

        with open(filePath, 'w') as file:
            for question, answer in zip(questions, answer):
                file.write(f"{question}{answer}\n")

        key = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_EAX)
        mensage = openFile(filePath)
        plaintext = mensage
        cipherMessage, tag = cipher.encrypt_and_digest(plaintext)

    elif option == 4:
        selectKey = input("digite o nome da sonda que voce deseja criar uma assinatura")





    elif option == 6:
        clear()
        break
