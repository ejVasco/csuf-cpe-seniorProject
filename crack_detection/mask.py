import cv2
import torch
import numpy as np
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator
from colorama import Fore, Style

# variables for sam model
sam_checkpoint = "sam_vit_h_4b8939.pth" # path to model or just file since same DIR
model_type = "vit_h"
device = "cuda" if torch.cuda.is_available() else "cpu" 

#------------------------------------------------
def main(input:str, out:str, preview:bool) -> None:
    # initialize sam model for creating the mask
    print(f"{Fore.WHITE}Loading SAM model...{Style.RESET_ALL}")
    sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
    sam.to(device=device)
    mask_generator = SamAutomaticMaskGenerator(sam)
    print(f"    {Fore.GREEN}SAM model LOADED ✔{Style.RESET_ALL}")
    def process_frame(frame):
        masks = mask_generator.generate(frame)
        # assuming largest mask is the ground
        if masks:
            # find said largest mask
            largest_mask = max(masks, key=lambda m: np.sum(m['segmentation']))
            mask = largest_mask['segmentation'].astype(np.uint8) * 255
            # apply mask to frame
            result = cv2.bitwise_and(frame, frame, mask=mask)
        else:
            result = frame        
        return result
    print(f"{Fore.WHITE}Starting Video Capture...{Style.RESET_ALL}")
    capture = cv2.VideoCapture(input)
    print(f"    {Fore.GREEN}Video Capture Started ✔{Style.RESET_ALL}")
    # total frames used to keep track of progress
    total_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    # use dimensions and fps of og video
    frame_width = int(capture.get(3))
    frame_height = int(capture.get(4))
    fps = int(capture.get(cv2.CAP_PROP_FPS))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v') # I keep getting an error on this line, but i mean... its working
    output = cv2.VideoWriter(out, fourcc, fps, (frame_width, frame_height))

    print(f"{Fore.WHITE}Beginning Processing...{Style.RESET_ALL}")
    curr_frame = 0
    while capture.isOpened():
        ret, frame = capture.read()
        copy = np.copy(frame)
        if not ret:
            break
        processed_frame = process_frame(frame)
        output.write(processed_frame)
        if preview:
            cv2.imshow("masked", processed_frame)
            cv2.imshow("og", copy)
            key = cv2.waitKey(1) & 0xFF  # Capture keyboard event
            if key == ord('q'):  # Allow quitting with 'q'
                break
        curr_frame = curr_frame+1
        print(f"    {Fore.WHITE}Progress: {Fore.CYAN}{curr_frame}/{total_frames}{Style.RESET_ALL}")
    capture.release()
    output.release()
    cv2.destroyAllWindows()   
    print(processing_complete + f"{Fore.CYAN}{out}{Fore.GREEN} ✔{Style.RESET_ALL}")
#------------------------------------------------
processing_complete = f'''{Fore.WHITE}Processing complete, masked video saved as: {Style.RESET_ALL}'''
argument_error = f'''
    {Fore.RED}ERROR: Invalid usage/incorrect number of arguments
    {Fore.WHITE}See Usage:
        {Fore.CYAN}python mask.py [input].mp4 [output_mask (default=output_mask)].mp4 [preview bool (default=0)]
    {Fore.WHITE}Example:
        {Fore.CYAN}python mask.py testvideo.mp4 testvideomask.mp4 0{Style.RESET_ALL}
'''
#------------------------------------------------
# converts str to bool, if invalid argument, default is false
def str_to_bool(s):
    return s.lower() in ("true", "1", "yes", "y", "t")
# handles arguments and defaults
if __name__ == "__main__":
    import sys
    # process is slow so previewing it is not very useful
    if len(sys.argv) >= 4:
        temp = str_to_bool(sys.argv[3])
        main(sys.argv[1], sys.argv[2], temp)

    elif len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2], False)

    elif len(sys.argv) == 2:
        main(sys.argv[1], "output_mask.mp4", False)
        # main(sys.argv[1], "output_mask.mp4", True)
    else:
        print(argument_error)
