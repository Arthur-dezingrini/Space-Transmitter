import os


def clear():
    os.system("cls")

def FileExist (name):
    if os.path.isdir(name):
        pass
    else:
        os.mkdir(name)

def openFile (file):
    key_file = open(file, "rb")
    key_data = key_file.read()
    key_file.close()
    return key_data
