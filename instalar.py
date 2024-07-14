import os
from time import sleep

class Instalador:
    def __init__(self):
        self.requirements_exists = os.path.exists("requirements.txt")
 
    def pip_install(self):
        os.system("pip install -r requirements.txt --break-system-packages")


    def pip_update(self):
        os.system("pip install --upgrade pip")


    def instalar(self):
        if (self.requirements_exists is False):
            raise FileNotFoundError("ESTÀ FALTANDO O ARQUIVO requirements.txt")

        self.pip_update()
        self.pip_install()



if __name__ == "__main__":
    print("Instalando os arquivos necessários...")
    sleep(1)
    installer = Instalador()
    installer.instalar()
    print("Dependencias instaladas com sucesso!")
