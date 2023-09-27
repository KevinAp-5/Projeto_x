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
    
    def get_json(self):
        positon = dict()
        with open(f'{self.path}/position.json', 'r+') as position_json:
            position = load(position_json)
            self.can_delete = True
            position_json.close()
        return position

    def delete_position(self):        
        for file in glob(f'{self.path}/position*.json'):
            os.remove(file)
        return True

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

    def move(self):
        x = 1250
        y = 570

        if 'win' in platform:
            while True:
                tab_name = WindowManager().window_title()
                if 'bet' in tab_name:
                    break
                else:
                    print('aguardand nalna ')
