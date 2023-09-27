import os

def clear():
    os.system("cls")

def FileExist (name):
    if os.path.isdir(name):
        pass
    else:
        os.mkdir(name)

def openFile (file, modo):
    key_file = open(file, modo)
    key_data = key_file.read()
    key_file.close()
    return key_data

def sendFile (client, FileName, FileContent):
    client.send(FileName.encode())
    client.send(FileContent)

def CreateFile (name):
    if os.path.isfile(name):
        pass
    else:
        open(name, "w")