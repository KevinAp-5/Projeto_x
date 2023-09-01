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
        pyautogui.PAUSE = 0.01
        manager = FileManager()
        manager.path = '.'  # Point for test json
        self.manager = manager

    def get_both(self, x_y=True):
        pos_dict = self.manager.get_position()
        if pos_dict is False:
            return False
        else:
            pos_dict = list(pos_dict.items())

        if x_y is True:  # return x, y
            pos_dict = pos_dict[:2]
        else:  # return width, height
            pos_dict = pos_dict[2:]

        x, y = pos_dict[0][1], pos_dict[1][1]
        return x, y

    def move(self, x, y):
        a = self.get_both()
        x, y = None, None

        if a is False:
            return False
        else:
            x, y = a[0], a[1]

        try:
            pyautogui.moveTo(x, y)
        except pyautogui.FailSafeException:
            print('saída de segurança acionada.')
            exit()


class Flow:
    def __init__(self):
        ...

    def main(self):
        mouse = MoveMouse()
        i = 0
        x, y = 0, 0
        while True:
            i = mouse.get_both()

            if type(i) != bool:
                x, y = i[0], i[1]
                break
            else:
                print('aguardando arquivo\t', end='\r', flush=True)
                sleep(0.1)

        while True:
            mouse.move(x, y)
            try:
                sleep(0.1)
            except KeyboardInterrupt:
                exit()
        mouse.position_update()


class WindowManager:
    def window_title(self):
        hWnd = windll.user32.GetForegroundWindow()
        length = windll.user32.GetWindowTextLengthW(hWnd)
        buf = create_unicode_buffer(length + 1)
        windll.user32.GetWindowTextW(hWnd, buf, length + 1)

        if buf.value:
            return str(buf.value)


if __name__ == '__main__':
    x = Flow().main()
    #x.move()
