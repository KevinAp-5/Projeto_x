import os
from time import sleep
import json
from random import randint

def create_x():
    x = {'x': 123, 'y': randint(-5000, 5000), 'width': 1359, 'height': 1011}
    return x

path = f'{os.path.expanduser("~")}/Downloads/position.json'

while True:
    writer = json.dumps(create_x(), indent=4)
    if os.path.exists(path) is False:
        with open(path, 'w') as file:
            file.write(writer)
            print('json criado')
        try:
            sleep(2)
        except KeyboardInterrupt:
            exit()
    else:
        print('aguardando delete...')
        try:
            sleep(2)
        except KeyboardInterrupt:
            print('closing.')
            exit()
    print()
