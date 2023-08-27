from json import load
import os
import pyautogui
from sys import platform
from glob import glob
from time import sleep

if 'win' in platform:
    from ctypes import wintypes, windll, create_unicode_buffer
    from pywinauto import Desktop, Aplication


class FileManager:
    def __init__(self):
        self.home = os.path.expanduser('~')
        self.path = self.home + '/Downloads'
        self.can_delete = False

    def exist_position(self):
        if os.path.exists(f'{self.path}/position.json'):
            self.can_delete = False
            return True
        else:
            return False

    def get_json(self):
        position = dict()
        with open(f'{self.path}/position.json', 'r+') as position_json:
            position = load(position_json)
            print('Posição capturada.')
            self.can_delete = True
            position_json.close()
        return position

    def delete_position(self):
        if self.can_delete is True:
            for file in glob(f'{self.path}/position*.json'):
                os.remove(file)
            print('Arquivo removido.')
            return True
        else:
            print("Não é possível remover arquivo.")
            return False

    def get_position(self):
        if self.exist_position() is True:
            my_position = self.get_json()
            self.delete_position()
            print(my_position)
            return my_position
        else:
            return False


class MoveMouse:
    def __init__(self):
        pyautogui.PAUSE = 0.2
        manager = FileManager()
        manager.path = '.'  # Point for test json
        self.position = manager.get_position()

    def get_both(self, x_y=True):
        a = list(self.position.items())
        if x_y is True:  # return x, y
            a = a[:2]
        else:  # return width, height
            a = a[2:]

        x, y = a[0][1], a[1][1]
        return x, y

    def move(self):
        x, y = self.get_both()
        pyautogui.moveTo(x, y)


if __name__ == '__main__':
    x = MoveMouse()
    print(x.position)
    x.get_both(False)
    #x.move()
