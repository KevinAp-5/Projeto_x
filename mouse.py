from json import load
import os
import pyautogui

class FileManagement:
    def __init__(self):
        self.home = os.path.expanduser('~')
        self.downloads = self.home + '/Downloads'
        self.can_delete = False

    def exist_position(self):
        if os.path.exists(f'{self.downloads}/position.json'):
            self.can_delete = False
            return True
        else:
            return False

    def get_json(self):
        position = dict()
        with open(f'{self.downloads}/position.json', 'r+') as position_json:
            position = load(position_json)
            print('Posição capturada.')
            self.can_delete = True
            position_json.close()
        return position

    def delete_position(self):
        if self.can_delete is True:
            try:
                os.remove(f'{self.downloads}/position.json')
            except FileNotFoundError:
                print('Arquivo não encontrado!!')
                return False
            print('File removed.')
            return True
        else:
            print("Não é possível remover arquivo.")
            return False
