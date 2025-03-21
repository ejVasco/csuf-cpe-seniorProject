import cv2
import torch
import numpy as np
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator
from colorama import Fore, Style

def main(input : str, out: str, preview: bool) -> None:
    # loading sam model
    sam_checkpoint = "sam_vit_h_4b8939.pth"  # path to sam
    model_type = "vit_h"
    device = "cuda" if torch.cuda.is_available() else "cpu" # device to use for processing

    sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
    sam.to(device=device)
    mask_generator = SamAutomaticMaskGenerator(sam)

    # function will process the frames, to create a mask for each frame
    def process_frame(frame):
        copy = np.copy(frame)
        masks = mask_generator.generate(frame)
        # assumes largest mask is the ground 
        if masks:
            largest_mask = max(masks, key=lambda m: np.sum(m['segmentation']))
            mask = largest_mask['segmentation'].astype(np.uint8) * 255
            # apply mask
            result = cv2.bitwise_and(frame, frame, mask=mask)
        else:
            result = frame
        if preview == True:
            cv2.imshow("masked", result)
            cv2.imshow("og", copy)
        return result

    # process video frames
    capture = cv2.VideoCapture(input)
    frame_width = int(capture.get(3))
    frame_height = int(capture.get(4))
    fps = int(capture.get(cv2.CAP_PROP_FPS))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output = cv2.VideoWriter(out, fourcc, fps, (frame_width, frame_height))

    while capture.isOpened():
        ret, frame = capture.read()
        if not ret:
            break
        
        processed_frame = process_frame(frame)
        output.write(processed_frame)

    capture.release()
    output.release()
    cv2.destroyAllWindows()
    processing_complete = f'''
    {Fore.WHITE}Processing complete, masked video saved as: {Fore.CYAN}{out}
'''
    print(processing_complete)


#------------------------------------------------

argument_error = f'''
    {Fore.RED}ERROR: Invalid usage/incorrect number of arguments
    {Fore.WHITE}See Usage:
        {Fore.CYAN}python mask.py [input].mp4 [output_mask (default=output_mask)].mp4 [preview bool (default=0)]
    {Fore.WHITE}Example:
        {Fore.CYAN}python mask.py testvideo.mp4 testvideomask.mp4 0{Style.RESET_ALL}
'''

#------------------------------------------------

# converts to bool, if invalid argument, default is false
def str_to_bool(s):
    return s.lower() in ("true", "1", "yes", "y", "t")

# handles arguments and defaults
if __name__ == "__main__":
    import sys

    if len(sys.argv) >= 4:
        temp = str_to_bool(sys.argv[3])
        main(sys.argv[1], sys.argv[2], temp)

    elif len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2], False)

    elif len(sys.argv) == 2:
        main(sys.argv[1], "output_mask.mp4", False)

    else:
        print(argument_error)
