from colorama import Fore, Style
import cv2
import numpy
import time

#--------------------------------------------------------------------
# functions for specific filetype processing
def webcam_process()-> None:
    print("webcam start")
    cap = cv2.VideoCapture(0) # 0 passes the webcam as video capture
    print("webcam vid capture:")
    while True:
        _, frame = cap.read()
        cv2.imshow("webcam live", frame)
        if break_key_pressed:
            return
def video_process() -> None:
    pass
def image_process() -> None:
    pass

#--------------------------------------------------------------------
# other functions

# returns true if break key pressed
def break_key_pressed() -> bool:
    return cv2.waitKey(1) == ord ('\\')
#--------------------------------------------------------------------
# functions for file type detection

# returns true if in_file is an image, else false
def IsImage(in_file) -> bool:
    img = cv2.imread(in_file)
    return img is not None 
# returns true if in_file can be opened as video capture, else false
def IsVideo(in_file) -> bool:
    cap = cv2.VideoCapture(in_file)
    if cap.isOpened():
        cap.release
        return True
    return False
#--------------------------------------------------------------------

def main(input) -> None:
    print(welcome_message)
    if input == "webcam":
        print("webcam")
        webcam_process()
    elif IsVideo(input):
        print("video")
        cap = cv2.VideoCapture(input)
    elif IsImage(input):
        print("image")
        cap = cv2.imread(input)
    else:
        print(invalid_file_error)
        return
    print(goodbye_message)
#--------------------------------------------------------------------
# string literals for ASCII art boxes below here

goodbye_message = f'''
temp goodbye
'''
hex_color = "#8000FF"  # Purple
r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
welcome_message = f'''
{Fore.YELLOW}   +---+
   | {Fore.WHITE}Script written by Esteban Vasco{Fore.YELLOW} |
   | {Fore.WHITE}in collaboration with:{Fore.YELLOW} |
   | {Fore.WHITE}Devin Lai{Fore.YELLOW} |
   | {Fore.WHITE}Wyatt Allen{Fore.YELLOW} |
   | {Fore.WHITE}Mason Phan{Fore.YELLOW} |
   | {Fore.WHITE}For Senior Project{Fore.YELLOW} |
   | {Fore.WHITE}At California State University of Fullerton{Fore.YELLOW} |
   +---------------------------------------------+{Style.RESET_ALL}
'''
missing_argument_error = f'''
{Fore.YELLOW}   +------------------------------------------+
   | {Fore.RED}ERROR: No input file or webcam argument. {Fore.YELLOW}|
   | {Fore.WHITE}To use this script:                      {Fore.YELLOW}|
   | {Fore.CYAN}> python universal.py FILE               {Fore.YELLOW}|
   | {Fore.WHITE}or                                       {Fore.YELLOW}|
   | {Fore.CYAN}> python universal.py webcam             {Fore.YELLOW}|
   | {Fore.WHITE}FILE may be a video or picture.          {Fore.YELLOW}|
   | {Fore.WHITE}Once program is running press \\ to exit  {Fore.YELLOW}|
   +------------------------------------------+{Style.RESET_ALL}
'''
invalid_file_error = f'''
{Fore.YELLOW}   +------------------------------------------------+
   | {Fore.RED}ERROR: Invalid file or script can't read file. {Fore.YELLOW}|
   | {Fore.WHITE}To use this script:                            {Fore.YELLOW}|
   | {Fore.CYAN}> python universal.py FILE                     {Fore.YELLOW}|
   | {Fore.WHITE}or                                             {Fore.YELLOW}|
   | {Fore.CYAN}> python universal.py webcam                   {Fore.YELLOW}|
   | {Fore.WHITE}FILE may be a video or picture.                {Fore.YELLOW}|
   | {Fore.WHITE}Once program is running press \\ to exit        {Fore.YELLOW}|
   +------------------------------------------------+{Style.RESET_ALL}
'''

#---------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        # kinda ASCII art box with r for a raw string b/c of the \
        print(missing_argument_error)
    else:
        main(sys.argv[1])
