import time
import os
from pyfiglet import Figlet
from art import *


def anime_hello():
    os.system('cls')

    print('               /\_/\               \n              ( o.o )\n               > ^ <')
    # print('\n')

    art = text2art("welcome   to  'Pet Shop'", sep=None)
    print(art, sep=None)


if __name__ == "__main__":
    anime_hello()
