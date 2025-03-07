from colorama import Fore, Style # color for error message
import cv2
import numpy as np
import time

# -----------------------------------------------
def main(capture, preview: int) -> None:
    print(welcome_message + capture)
    if capture == 'webcam':
        wc = True
        cap = cv2.VideoCapture(0)
    else:
        wc = False
        cap = cv2.VideoCapture(capture)
    if not cap.isOpened():
        if wc:
            print(wb_capture_error)
        else:
            print(video_capture_error)
        return
    
# -----------------------------------------------
# strings for different messages
welcome_message = f'''{Fore.CYAN}
Starting crack detection on: {Style.RESET_ALL}'''
wb_capture_error = f'''{Fore.RED}
ERROR: Webcam capture failed{Fore.YELLOW}
Make sure webcam is properly connected/on.
Try testing the camera in another program or browser.
'''
video_capture_error = f'''{Fore.RED}
ERROR: Video capture failed{Fore.YELLOW}
Make sure the video file/path is typed exactly.
Try testing the video in a video player.
'''
usage_error = f'''{Fore.RED}
ERROR: Invalid script usage{Fore.YELLOW}
See README.md or run {Fore.CYAN}python actual.py -h{Fore.YELLOW} to see usage.{Style.RESET_ALL}
'''
help_message = f'''{Fore.YELLOW}
Script takes one required argument and then optional arguments, see usage:{Fore.CYAN}
    python actual.py [capture] [previewType]{Fore.BLUE}
[capture] can be: [videoFile], [path]/[videoFile], webcam
[previewType] can be: 0, 1, 2{Fore.YELLOW}
    0 -> (default) before and after processing preview
    1 -> after preview
    2 -> no preview{Style.RESET_ALL}
'''
# -----------------------------------------------
help_options = ['h', '-h', '--h', 'help', '-help', '--help']
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2: # at least one argument
        print(usage_error)
        sys.exit(1)
    capture_source = sys.argv[1] # first arg is cap source
    if capture_source in help_options: # check user help prompt
        print(help_message)
        sys.exit(0)
    # check preview mode arg
    preview_mode = 0  # default mode    
    if len(sys.argv) > 2:
        try:
            preview_mode = int(sys.argv[2])
            if preview_mode not in [0, 1, 2]:  # valid modes
                raise ValueError
        except ValueError:
            print(usage_error)
            sys.exit(1)
    main(capture_source, preview_mode)
