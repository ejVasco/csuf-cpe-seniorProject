import cv2
import time
import torch
import numpy as np
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator
from pathlib import Path

#------------------------------------------------

# variables for debugging
debug : bool =  True
if debug: print(f"\n  Debugging on\n")
output_vid : bool = True 
# sam variables
sam_checkpoint = "sam_vit_h_4b8939.pth"
model_type = "vit_h"
# what device to use for processing
device = "cuda" if torch.cuda.is_available() else "cpu"
if debug: print(f"device: {device}")

#------------------------------------------------

def main(input:str, mode:str):

    # preview mode handling
    if debug: print("figuring out input mode")
    in_prev = 'i' in mode
    out_prev = 'o' in mode
    m_prev = 'm' in mode
    if debug: print(f"iom preview: {in_prev} {out_prev} {m_prev}")

    # loading sam
    if debug: print("loading sam and sam auto mask gen")
    sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
    sam.to(device=device)
    mask_generator = SamAutomaticMaskGenerator(sam)
    if debug: print ("sam loaded and auto mask gen'ed")

    # process frame is in here bc it uses the mask_generator
    def process_frame(frame):

        # input preview        
        if in_prev: copy1 = np.copy(frame)

        # masking processing
        masks = mask_generator.generate(frame)
        if masks:
            # find said largest mask
            largest_mask = max(masks, key=lambda m: np.sum(m['segmentation']))
            mask = largest_mask['segmentation'].astype(np.uint8) * 255
            # apply mask to frame
            frame = cv2.bitwise_and(frame, frame, mask=mask) # blacks out parts of frame
        # if no largest mask is found, assume whole image is the ground

        # masked preview 
        if m_prev: copy2 = np.copy(frame)
        
        # crack detection processing
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # convert frame to grayscale
        frame = cv2.GaussianBlur(frame, (7,7), 0) # blurs frame
        frame = cv2.Canny(frame, 50, 150) # edge detects frame
        contours, _ = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # finds contours
        frame = np.zeros((frame.shape[0], frame.shape[1], 3), dtype=np.uint8) # turns frame to a black background
        cv2.drawContours(frame, contours, -1, (255, 255, 255), 1)  # draws white contours on black frame

        # output preview
        result = np.copy(frame)

        return frame
    
    if debug: print("starting vid capture")
    capture = cv2.VideoCapture(input)
    if debug: print("videocapture started")

    # get total frames to use for percent calc for percentage progress bar
    total_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    if debug: print(f"total frames found: {total_frames}")

    # prepare to make output vid
    if output_vid:
        if debug: print ("getting og vid properties to use for output vid")
        frame_width = int(capture.get(3))
        frame_height = int(capture.get(4))
        if debug: print (f"vid dimensions: x={frame_width} y={frame_height}")
        fps = int(capture.get(cv2.CAP_PROP_FPS))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v') # I keep getting an error on this line, but i mean... its working
        out = "processed_" + Path(input).expanduser().name # processed_inputfile.mp4
        output = cv2.VideoWriter(out, fourcc, fps, (frame_width, frame_height))
        if debug: print (f"ready to output video to {out}")

    # processing loop
    curr_frame = 0 # current frame
    if debug: print("beginning processing")
    while capture.isOpened():

        # capture read
        ret, frame = capture.read()
        if not ret:
            break # breaks if capture failed to get ret (and frame)

        # process
        processed_frame = process_frame(frame)

        # creating output vid if enabled
        if output_vid : output.write(processed_frame)

        # if preview, press q to quit
        if in_prev or m_prev or out_prev:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # progress output
        curr_frame = curr_frame + 1
        print(f"progress: {curr_frame}/{total_frames}")

    # release cv2 windows if open
    capture.release()
    output.release()
    cv2.destroyAllWindows()

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