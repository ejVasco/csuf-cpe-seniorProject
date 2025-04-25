from colorama import Fore, Style # color for error message
import cv2
import time
import torch
import numpy as np
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator
from pathlib import Path
# variables for debugging
debug : bool =  True 
output_vid : bool = True 
# sam variables
sam_checkpoint = "sam_vit_h_4b8939.pth"
model_type = "vit_h"
# what device to use for processing
device = "cuda" if torch.cuda.is_available() else "cpu"
#------------------------------------------------
def main(input:str, mode:str):
    # preview mode handling
    if debug: print("figuring out input mode")
    in_prev = 'i' in mode
    out_prev = 'o' in mode
    m_prev = 'm' in mode
    if debug: print("iom preview: " + str(in_prev) + str(out_prev) + str(m_prev))

    if debug: print("loading sam and sam auto mask gen")
    sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
    sam.to(device=device)
    mask_generator = SamAutomaticMaskGenerator(sam)
    if debug: print ("sam loaded and auto mask gen'ed")

    # process frame is in here bc it uses the mask_generator
    def process_frame(frame):
        masks = mask_generator.generate(frame)
        if masks:
            # find said largest mask
            largest_mask = max(masks, key=lambda m: np.sum(m['segmentation']))
            mask = largest_mask['segmentation'].astype(np.uint8) * 255
            # apply mask to frame
            result = cv2.bitwise_and(frame, frame, mask=mask)
        else:
            result = frame        
        return result
    if debug: print("starting vid capture")
    capture = cv2.VideoCapture(input)
    if debug: print("videocapture started")
    # get total frames to use for percent calc for percentage progress bar
    total_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    # get og dimensions and fps to use for output vid
    if output_vid:
        if debug: print ("getting og vid properties to use for output vid")
        frame_width = int(capture.get(3))
        frame_height = int(capture.get(4))
        fps = int(capture.get(cv2.CAP_PROP_FPS))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v') # I keep getting an error on this line, but i mean... its working
        output = cv2.VideoWriter(out, fourcc, fps, (frame_width, frame_height))



    
        
#------------------------------------------------
# strings for outputting
help_s = 'help placeholder'
# handling arguments
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Program requires arguments to run")
        print(help_s)
    elif Path(sys.argv[1]).is_file():
        if len(sys.argv) == 2:
            main(sys.argv[1], "")
        else:
            main(sys.argv[1], sys.argv[2])
    else:
        print("Invalid filepath or could not verify file exists")
        print(help_s)