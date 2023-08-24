from json import load
import os
import pyautogui

class FileManagement:
    def __init__(self):
        self.home = os.path.expanduser('~')
        self.downloads = self.home + '/Downloads'
        self.can_delete = False
