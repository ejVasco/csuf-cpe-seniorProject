from colorama import Fore, Style # color for error message
import cv2
import time
import torch
import numpy as np
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator
#------------------------------------------------
def main(input:str, mode:int):
    if mode == 0:
        print('main in default mode confirmed')
    else:
        # print("mode is " + mode)
        pass
#------------------------------------------------
# strings for outputting
help_s = 'help placeholder'
help_args = ['h', 'help', '-h', '-help', '--h', '--help']
# functions to handle input
def file_exists(input:str) -> bool:
    return True
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Too few arguments")
        print(help_s)
    elif len(sys.argv) == 2:
        if sys.argv[1] in help_args:
            print(help_s)
        elif file_exists(sys.argv[1]):
            print('main in default mode?')
            main(sys.argv[1], 0)
    elif file_exists(sys.argv[1]) and sys.argv[2].isdigit():
        pass
    else:
        print("Invalid usage")
        print(help_s)