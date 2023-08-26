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
                for file in glob(f'{self.downloads}/position*.json'):
                    os.remove(file)
            except FileNotFoundError:
                print('Arquivo não encontrado!!')
                return False
            print('File removed.')
            return True
        else:
            print("Não é possível remover arquivo.")
            return False

    def get_position(self):
        my_position = ''
        if self.exist_position() is True:
            my_position = self.get_json()
        else:
            print('Arquivo não existe ainda.')

        self.delete_position()
        return my_position


class WindowManager:
    def window_title(self):
        hWnd = windll.user32.GetForegroundWindow()
        length = windll.user32.GetWindowTextLengthW(hWnd)
        buf = create_unicode_buffer(length + 1)
        windll.user32.GetWindowTextW(hWnd, buf, length + 1)

        if buf.value:
            return str(buf.value)


class MoveMouse:
    def __init__(self):
        pyautogui.PAUSE = 0.2
        manager = FileManager()
        manager.downloads = '.'  # Point for test json
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
        x, y = self.get_xy()
        pyautogui.moveTo(x, y)


if __name__ == '__main__':
    x = MoveMouse()
    print(x.position)
    x.get_both(False)
    #x.move()
