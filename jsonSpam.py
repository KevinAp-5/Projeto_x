import os
from time import sleep
import json

x = {'x': 123, 'y': 281, 'width': 1359, 'height': 1011}

writer = json.dumps(x, indent=4)

while True:
    if os.path.exists('position.json') is False:
        with open('position.json', 'w') as file:
            file.write(writer)
            print('json criado')
        try:
            sleep(2)
        except KeyboardInterrupt:
            continue
    else:
        print('aguardando...')
        try:
            sleep(2)
        except KeyboardInterrupt:
            print('closing.')
            exit()
    print()
