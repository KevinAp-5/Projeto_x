from json import load
import os
from os import get_terminal_size
import pyautogui
from sys import platform, argv
from glob import glob
from time import sleep
from pyperclip import copy
from plyer import notification

if 'win' in platform:
    from ctypes import wintypes, windll, create_unicode_buffer
#    from pywinauto import Desktop, Aplication


def get_argv():
    conf = [int(float(item.strip())) for item in argv[1:]]
    return conf[:3]


def printer(text):
    print(str(text).center(terminal_size()), end='\r', flush=True)


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
            printer('Procurando')
            self.can_delete = True
            position_json.close()
        return position

    def delete_position(self):
        if self.can_delete is True:
            for file in glob(f'{self.path}/position*.json'):
                os.remove(file)
            return True
        else:
            return False

    def get_position(self):
        if self.exist_position() is True:
            my_position = self.get_json()
            self.delete_position()
            return my_position
        else:
            return False


class MoveMouse:
    def __init__(self):
        pyautogui.PAUSE = 0.01
        manager = FileManager()
        self.manager = manager
        self.counter = 0

    def write(self, text):
        copy(text)
        sleep(0.1)
        pyautogui.hotkey('ctrl', 'v')

    def get_both(self, x_y=True, full=False):
        pos_dict = self.manager.get_position()
        if pos_dict is False:
            return False
        else:
            pos_dict = list(pos_dict.items())

        if full is True:
            return dict(pos_dict)

        if x_y is True:  # return x, y
            pos_dict = pos_dict[:2]
        else:  # return width, height
            pos_dict = pos_dict[2:]

        x, y = pos_dict[0][1], pos_dict[1][1]
        return x, y

    def move(self, x, y):
        filterr = argv[0]
        if 'mouse' in filterr:
            filterr = 2
        else:
            filterr = int(argv[0])

        a = self.get_both(full=True)
        if a is False:
            return False

        json_info = list(a.values())
        x, y = json_info[0], json_info[1]
        w, h = json_info[2], json_info[3]
        nome = json_info[4]

        if 'win' in platform:
            while 'bet' not in WindowManager().window_title():
                text = 'aguardando voltar para janela da bet'
                for x in range(3):
                    printer(str(text+'.'*x))
                    sleep(0.5)
                    if 'bet' in WindowManager.window_title():
                        break
                sleep(0.1)
        print()

        copy('')
        pyautogui.moveTo(1107)
        pyautogui.moveTo(y=575)
        pyautogui.hotkey('esc')
        pyautogui.hotkey('f3')
        partida = ' '.join(nome.split(' ')[:filterr])

        a = ' '.join(partida.split('GOL'))
        b = a.split(' ')[0]
        if len(b) <= 5:
            partida = a
        else:
            partida = b
#        notification.notify(title=partida, timeout=3)
        partida = ''.join(partida)
        printer(partida)
        print()
        self.counter += 1
        printer(f"Gols encontrados: {self.counter}")
        print()
        print()
        self.write(partida)
        sleep(0.1)
        pyautogui.click()
        sleep(0.009)
        pyautogui.click()
        try:
            sleep(5)
        except KeyboardInterrupt:
            exit()
        pyautogui.hotkey('f3')
        pyautogui.hotkey('backspace')
        sleep(0.1)
        pyautogui.hotkey('esc')


def terminal_size():
    return get_terminal_size()[0]


def banner(title):
    size = terminal_size()
    return f'{"="*size}\n{title.title().center(size)}\n{"="*size}'


def nice_line():
    line = '-' * int(terminal_size()*0.60)
    white_space = ' ' * int((terminal_size()/2) - (len(line)/2))
    line = f'{white_space}{line}{white_space}\n'
    sleep_time = 0.02

    for item in line:
        print(item, end='', flush=True)
        try:
            sleep(sleep_time)
        except KeyboardInterrupt:
            sleep_time = 0


class Flow:
    def __init__(self):
        print(banner('Mineirinho Scanner'))
        nice_line()
        filer = FileManager()
        filer.exist_position()
        filer.delete_position()

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
                printer('aguardando gol')
                try:
                    sleep(0.1)
                except KeyboardInterrupt:
                    exit()

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
        else:
            return ''


if __name__ == '__main__':
    x = Flow()
    x.main()
    #x.move()
