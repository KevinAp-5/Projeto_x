from source.clipboard import copy
from json import load
import os
from os import get_terminal_size
import pyautogui
from sys import platform, argv
from glob import glob
from time import sleep
from playsound import playsound

try:
    import threading
except ImportError:
    os.system("pip install thread")
    sleep(1)
    import threading


WINDOWS = False
if 'win' in platform:
    from ctypes import wintypes, windll, create_unicode_buffer
    WINDOWS = True


def terminal_size():
    return int(get_terminal_size()[0])


def get_argv():
    conf = [int(float(item.strip())) for item in argv[1:]]
    return conf[:3]


def banner(title):
    size = terminal_size()
    return f'{"="*size}\n{title.title().center(size)}\n{"="*size}'


def nice_line():
    line = '-' * int(terminal_size()*0.60)
    white_space = ' ' * int((terminal_size()/2) - (len(line)/2))
    line = f'{white_space}{line}{white_space}\n'
    sleep_time = 0.01

    for item in line:
        print(item, end='', flush=True)
        try:
            sleep(sleep_time)
        except KeyboardInterrupt:
            sleep_time = 0


class GetInput():
    def __init__(self):
        self.text = 'Você quer continuar? [S/n]\n'

    def get_answer(self):
        while True:
            try:
                Printer(self.text)
                x = int((terminal_size()/2)-1)
                self.text = input(' '*x)
                self.text = self.text.strip().lower()[0]
            except KeyboardInterrupt:
                exit()
            except IndexError:
                continue

            if self.text:
                return self.text


class Keyboard():
    def __init__(self):
        self.user_input = GetInput()

    def treat_input(self):
        while True:
            resume_pomodoro = self.user_input.get_answer()
            if resume_pomodoro == 's':
                Printer('Continuando.')
                break
            elif resume_pomodoro == 'n':
                Printer('\nAdeus!')
                exit()
            else:
                Printer('Resposta inválida! use [S/N]\n')
                self.reset()
        self.reset()

    def reset(self):
        self.user_input = GetInput()


class Printer:
    def __init__(self, text):
        print(str(text).center(terminal_size()), end='\r', flush=True)

    @staticmethod
    def clean():
        Printer(' '*terminal_size())


class FileManager:
    def __init__(self):
        self.home = os.path.expanduser('~')
        self.path = self.home + '/Downloads'
        self.can_delete = False
        self.doubleName = False
        self.nomeReserva = ''
        self.name3 = False

    def file_exists(self):
        return os.path.exists(f'{self.path}/position.json')

    def get_json(self):
        position = dict()

        if self.file_exists() is False:
            return False
        to_open = f'{self.path}/position.json'

        with open(to_open, 'r+', encoding='utf-8') as position_json:
            position = load(position_json)
            self.can_delete = True
            position_json.close()
        return position

    def delete_position(self):
        for file in glob(f'{self.path}/position*.json'):
            os.remove(file)
        return True

    def get_nome(self, json_info):
        raw_names = [
            [item for item in x.replace("GOL", "").split("\n") if item != ""]
            for x in json_info.values()
        ]

        nome1 = raw_names[0][0]
        nome2 = next((x for x in raw_names[1] if x != nome1))

        return self.escolhe_nome([nome1, nome2])

    def escolhe_nome(self, lista_nome):
        nome1, nome2 = lista_nome[0], lista_nome[1]
        if len(nome1) == 2:
            self.doubleName = True
            self.nomeReserva = nome1
            return nome2

        self.doubleName = False
        self.nomeReserva = ''

        if len(nome1) == 3:
            self.name3 = True
        else:
            self.name3 = False
        return nome1

def teamName(raw_info):
    return raw_info.split('\n')

def playsd():
    playsound('sound.mp3')


class MoveMouse:
    def __init__(self):
        pyautogui.PAUSE = 0.01
        manager = FileManager()
        self.manager = manager
        self.seconds = 0

    def write(self, text):
        copy(text)
        sleep(0.2)
        pyautogui.hotkey('ctrl', 'v')
        return True

    def clean_clipboard(self):
        copy('')

    def partida_name(self, nome):
        self.manager.delete_position()
        return nome.lower()

    def open_search(self):
        self.clean_clipboard()
        sleep(0.3)
        pyautogui.hotkey('esc')
        pyautogui.hotkey('f3')
        return True

    def click(self):
        sleep(0.35)  ######### 0.3s, mudar só o numero entre parenteses
        pyautogui.click()

    def clean_search(self):
        sleep(1.5)
        pyautogui.hotkey('f3')
        pyautogui.hotkey('backspace')
        sleep(0.1)
        pyautogui.hotkey('esc')

    def move_mouse(self, x=1270, y=570):
        pyautogui.moveTo(x)
        pyautogui.moveTo(y=y)

    def main(self, x=1270, y=580):

#        if WINDOWS is True:
#            WindowManager.bet_loop()

        nome_time = self.partida_name(self.gol_info_loop())

        if self.manager.doubleName is True:
            nome_time_show = self.nomeReserva

        nome_time_show = nome_time
        Printer(f'{nome_time_show} - {self.seconds:.2f}s')
        print()
        print()

        threading.Thread(target=playsd).start()
        self.open_search()
        sleep(0.1)

        self.move_mouse(x, y)
        self.write(nome_time)
      
        self.click()
        if self.manager.name3 is True:
            self.click()

        self.clean_search()

    def gol_info_loop(self):
        counter = 0
        while True:
            alert = ' - Espera alta, verifique o site ou programa'
            gol_info = self.manager.get_json()
            if gol_info is False:
                if counter <= 200:
                    alert = ''
                Printer(f'aguardando gol {counter:.2f}s {alert}')
                try:
                    sleep(0.2)
                except KeyboardInterrupt:
                    print()
                    Keyboard().treat_input()
                    FileManager().delete_position()
                    counter = 0
                counter += 0.2
            else:
                Printer.clean()
                nome = self.manager.get_nome(gol_info)
                self.seconds = counter
                return nome


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

    def check_tab_name(self):
        tab_name = WindowManager().window_title()
        x = tab_name.split(' ')[0].lower()
        if 'bet' in x:
            return True
        else:
            return False

    def bet_loop(self):
        while True:
            if self.check_tab_name() is False:
                print('aguardando voltar para bet', '\r', flush=True)
            else:
                break
            try:
                sleep(0.2)
            except KeyboardInterrupt:
                print()
                Keyboard().treat_input()


class Main:
    def __init__(self):
        print(banner('Mineirinho Scanner'))
        nice_line()

    def run(self):
        FileManager().delete_position()
        sleep(0.5)

        try:
            while True:
                MoveMouse().main()
        except KeyboardInterrupt:
            print()
            Keyboard().treat_input()


if __name__ == '__main__':
    Main().run()
