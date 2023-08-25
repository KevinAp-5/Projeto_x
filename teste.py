from ctypes import wintypes, windll, create_unicode_buffer
from time import sleep

def getForegroundWindowTitle():
    hWnd = windll.user32.GetForegroundWindow()
    length = windll.user32.GetWindowTextLengthW(hWnd)
    buf = create_unicode_buffer(length + 1)
    windll.user32.GetWindowTextW(hWnd, buf, length + 1)

    if buf.value:
        return buf.value
    else:
        return None


if __name__ == '__main__':
    print('wainting')
    sleep(2)
    x = getForegroundWindowTitle()
    print(f'Janela ativa: {x}')
