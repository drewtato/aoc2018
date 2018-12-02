import requests
import sys
import os
import time
import shutil

day = sys.argv[1]
try:
    os.mkdir(f'day{day}')
except FileExistsError:
    pass

if not os.path.isfile(f'day{day}/day{day}.py'):
    shutil.copyfile('dayx.py', f'day{day}/day{day}.py')

go = '''
                     GGGGGGGGGGGGG         OOOOOOOOO     
                  GGG::::::::::::G       OO:::::::::OO   
               GG:::::::::::::::G     OO:::::::::::::OO 
             G:::::GGGGGGGG::::G    O:::::::OOO:::::::O
           G:::::G       GGGGGG    O::::::O   O::::::O
         G:::::G                  O:::::O     O:::::O
        G:::::G                  O:::::O     O:::::O
       G:::::G    GGGGGGGGGG    O:::::O     O:::::O
      G:::::G    G::::::::G    O:::::O     O:::::O
     G:::::G    GGGGG::::G    O:::::O     O:::::O
    G:::::G        G::::G    O:::::O     O:::::O
    G:::::G       G::::G    O::::::O   O::::::O
    G:::::GGGGGGGG::::G    O:::::::OOO:::::::O
    GG:::::::::::::::G     OO:::::::::::::OO 
     GGG::::::GGG:::G       OO:::::::::OO   
       GGGGGG   GGGG         OOOOOOOOO 
'''

with open('auth', 'r') as auth:
    cookies = {'session': auth.read()}

while True:
    input = requests.get(f'https://adventofcode.com/2018/day/{day}/input', cookies=cookies)
    if input.status_code != 200:
        print(f'{input.status_code}, retry in 10')
        time.sleep(10)
    else:
        print('200, saving file!')
        print(go)
        with open(f'day{day}/input.txt', 'wb') as f:
            f.write(input.content)
        break