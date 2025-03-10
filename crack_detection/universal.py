from colorama import Fore, Style
import cv2
import numpy
import time

#--------------------------------------------------------------------
#general process fram func
def frame_proc(frame):
    copy = numpy.copy(frame)
    gray = cv2.cvtColor(copy, cv2.COLOR_BGR2GRAY)
    blue = cv2.GaussianBlur(gray, (7,7),0)
    edges = cv2.Canny(blue, 50,150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(copy, contours, -1, (0,255,0),-1)
    cv2.imshow("Processed",copy)

# vid/cam loop
def loop_proc(window_name: str, cap: cv2.VideoCapture):
    while (True):
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame")
            break
        frame_proc(frame)
        cv2.imshow(window_name, frame)
        if break_key_pressed():
            break
    cap.release()
    cv2.destroyAllWindows()
        


# functions for specific filetype processing
def webcam_process() -> None:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
    loop_proc("Webcam", cap)
    print("Debug: Exiting webcam_process()")


#--------------------------------------------------------------------
# other functions

# returns true if break key pressed
def break_key_pressed() -> bool:
    return cv2.waitKey(1) & 0xFF == ord('q')
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
        cap.release()
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
# alternate messages
# goodbye_message = "test bye"
# welcome_message = "test welcome"
# missing_argument_error = "test missing arg error"
# invalid_file_error = "test invalid file error"

#---------------------------------------------------------------------
# def test():
#     print('webcam test')
#     cap = cv2.VideoCapture(0) # 0 passes the webcam as video capture
#     while True:
#         _, frame = cap.read()
#         cv2.imshow("webcam live", frame)
#         if cv2.waitKey(1) == ord ('q'):
#             cap.release()
#             return



if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        # kinda ASCII art box with r for a raw string b/c of the \
        print(missing_argument_error)
    else:
        # test()
        main(sys.argv[1])
