import os
from time import sleep
import threading

class Instalador:
    def __init__(self):
        self.requirements_exists = os.path.exists("requirements.txt")

    @staticmethod
    def start_message():
        print("Instalando os arquivos necessários...")
 
    def pip_install(self):
        self.pip_update()
        os.system("pip install -r requirements.txt --break-system-packages")


    def pip_update(self):
        os.system("pip install --upgrade pip")


    def instalar(self):
        if (self.requirements_exists is False):
            raise FileNotFoundError("ESTÀ FALTANDO O ARQUIVO requirements.txt")

        self.pip_update()
        self.pip_install()



if __name__ == "__main__":
    installer = Instalador()
    threading.Thread(target=installer.start_message).start()
    installer.instalar()
