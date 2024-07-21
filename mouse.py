import os
import json
import pyautogui
import threading
from sys import argv, platform
from time import sleep
from glob import glob
from playsound import playsound
from clipboard import copy
from os import get_terminal_size

sound_enabled = True  # Variável global para rastrear o estado do som

class Utilities:
    @staticmethod
    def terminal_size():
        try:
            return int(get_terminal_size()[0])
        except OSError:
            print("Rode o programa em outro terminal")

    @staticmethod
    def get_argv():
        return [int(float(item.strip())) for item in argv[1:3]]

    @staticmethod
    def banner(title):
        size = Utilities.terminal_size()
        return f'{"=" * size}\n{title.title().center(size)}\n{"=" * size}'

    @staticmethod
    def nice_line():
        line = '-' * int(Utilities.terminal_size() * 0.60)
        white_space = ' ' * int((Utilities.terminal_size() / 2) - (len(line) / 2))
        line = f'{white_space}{line}{white_space}\n'
        sleep_time = 0.01

        for item in line:
            print(item, end='', flush=True)
            try:
                sleep(sleep_time)
            except KeyboardInterrupt:
                sleep_time = 0

    @staticmethod
    def play_sound():
        if sound_enabled:
            playsound('sound.wav')


class GetInput:
    def __init__(self):
        self.text = 'Você quer continuar? [S/n] - Som[P]\n'

    def get_answer(self):
        while True:
            try:
                print(self.text.center(Utilities.terminal_size()), end='\r', flush=True)
                x = int((Utilities.terminal_size() / 2) - 1)
                self.text = input(' ' * x).strip().lower()[0]
            except KeyboardInterrupt:
                exit()
            except IndexError:
                continue

            if self.text:
                return self.text


class Keyboard:
    def __init__(self):
        self.user_input = GetInput()

    def treat_input(self):
        global sound_enabled
        while True:
            resume_pomodoro = self.user_input.get_answer()
            if resume_pomodoro == 's':
                print()
                break
            elif resume_pomodoro == 'n':
                exit()
            elif resume_pomodoro == 'p':
                sound_enabled = not sound_enabled
                status = 'ativado' if sound_enabled else 'desativado'
                print(f'Som {status}.'.center(Utilities.terminal_size()), end='', flush=True)
                self.reset()
            else:
                print('Resposta inválida! use [S/N] - Som[P]\n'.center(Utilities.terminal_size()), end='\r', flush=True)
                self.reset()
        self.reset()

    def reset(self):
        self.user_input = GetInput()


class Printer:
    @staticmethod
    def clean():
        print(' ' * Utilities.terminal_size(), end='\r', flush=True)


class FileManager:
    def __init__(self):
        self.home = os.path.expanduser('~')
        self.path = os.path.join(self.home, 'Downloads')
        self.can_delete = False
        self.two_letters = False
        self.nome_reserva = ''
        self.name3 = False

    def file_exists(self):
        return os.path.exists(os.path.join(self.path, 'position.json'))

    def get_json(self):
        if not self.file_exists():
            return False

        with open(os.path.join(self.path, 'position.json'), 'r+', encoding='utf-8') as position_json:
            position = json.load(position_json)
            self.can_delete = True
        return position

    def delete_position(self):
        for file in glob(os.path.join(self.path, 'position*.json')):
            os.remove(file)
        return True

    def get_nome(self, json_info):
        raw_names = [
            [item for item in x.replace("GOL", "").split("\n") if item]
            for x in json_info.values()
        ]

        nome1 = raw_names[0][0]
        nome2 = next((x for x in raw_names[1] if x != nome1), None)

        return self.escolhe_nome([nome1, nome2])

    def escolhe_nome(self, lista_nome):
        nome1, nome2 = lista_nome[0], lista_nome[1]
        if len(nome1) == 2:
            self.two_letters = True
            self.nome_reserva = nome1
            return nome2

        self.two_letters = False
        self.nome_reserva = ''

        if len(nome1) == 3:
            self.name3 = True
        else:
            self.name3 = False
        return nome1


class MoveMouse:
    def __init__(self):
        pyautogui.PAUSE = 0.01
        self.manager = FileManager()
        self.seconds = 0
        self._sound_thread = threading.Thread(target=Utilities.play_sound)

    def write(self, text):
        copy(text)
        sleep(0.2)
        pyautogui.hotkey('ctrl', 'v')

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

    def click(self):
        sleep(0.35)
        pyautogui.click()

    def clean_search(self):
        sleep(1.7)
        pyautogui.hotkey('f3')
        pyautogui.hotkey('backspace')
        sleep(0.1)
        pyautogui.hotkey('esc')

    def move_mouse(self, x=1270, y=570):
        pyautogui.moveTo(x=x, y=y)

    def main(self, x=1270, y=580):
        nome_time = self.partida_name(self.gol_info_loop())
        nome_time_show = self.manager.nome_reserva if self.manager.two_letters else nome_time

        print(f'{nome_time_show} - {self.seconds:.2f}s'.center(Utilities.terminal_size()), end='\r', flush=True)
        print('\n')

        if sound_enabled:
            threading.Thread(target=Utilities.play_sound).start()
        self.open_search()
        sleep(0.1)

        self.move_mouse(x, y)
        self.write(nome_time)
        self.click()

        if self.manager.name3:
            self.move_mouse(x=1260)
            sleep(0.2)
            threading.Thread(target=pyautogui.click).start()

        print()
        threading.Thread(target=self.clean_search).start()

        Keyboard().treat_input()
        FileManager().delete_position()

    def gol_info_loop(self):
        counter = 0
        while True:
            gol_info = self.manager.get_json()

            if gol_info:
                Printer.clean()
                nome = self.manager.get_nome(gol_info)
                self.seconds = counter
                return nome

            alert = '' if counter <= 200 else ' - Espera alta, verifique o site ou programa'
            print(f'aguardando gol {counter:.2f}s {alert}'.center(
                Utilities.terminal_size()
                ), end='\r', flush=True)

            try:
                sleep(0.2)
            except KeyboardInterrupt:
                print()
                Keyboard().treat_input()
                FileManager().delete_position()
                counter = 0

            counter += 0.2

class Main:
    def __init__(self):
        print(Utilities.banner('Mineirinho Scanner'))
        Utilities.nice_line()

    def run(self):
        FileManager().delete_position()

        try:
            while True:
                MoveMouse().main()
        except KeyboardInterrupt:
            print()
            Keyboard().treat_input()


if __name__ == '__main__':
    Main().run()
