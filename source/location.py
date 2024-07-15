import pyautogui
from plyer import notification
from time import sleep


def get_position():
    while True:
        x, y = pyautogui.position()
        notification.notify(
            title='Posição do mouse',
            message='x={}, y={}'.format(x, y),
            timeout=2
            )

        try:
            sleep(2.5)
        except KeyboardInterrupt:
            print()
            return x, y


if __name__ == '__main__':
    print(get_position())
