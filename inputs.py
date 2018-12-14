import requests
import sys
import os
import time
import shutil

day = int(sys.argv[1])
try:
    os.mkdir(f'day{day:02}')
except FileExistsError:
    pass

if not os.path.isfile(f'day{day:02}/day{day:02}.py'):
    shutil.copyfile('dayx.py', f'day{day:02}/day{day:02}.py')
    shutil.copyfile('testinput.txt', f'day{day:02}/input.txt')

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

print('Enter to fetch input ', end='')
while True:
    input()
    input = requests.get(f'https://adventofcode.com/2018/day/{day}/input', cookies=cookies)
    if input.status_code != 200:
        print(f'{input.status_code}, retry on enter')
    else:
        print('200, saving file!')
        print(go)
        with open(f'day{day:02}/input.txt', 'wb') as f:
            f.write(input.content)
        break