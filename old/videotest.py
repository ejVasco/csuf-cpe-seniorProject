import cv2
import numpy as np
import time

def process_frame(frame):
    # filters
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    # edge detection
    edges = cv2.Canny(blur, 50, 150)
    # find n fill contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)    
    # overlap contours on frame
    cv2.drawContours(frame, contours, -1, (0, 255, 0), -1)
    return frame

def main(video_file): # must pass through video file when using script i.e. python script.py video-file
    # declare and open video
    cap = cv2.VideoCapture(video_file)
    # confirm video open
    if not cap.isOpened():
        print("eror: vid file no open :(")
        return
    # loop through frames
    while True:
        # retrieve frame from vid cap object
        ret, frame = cap.read()
        # if not retrieved
        if not ret:
            break
        # process frame
        overlap_image = process_frame(frame)
        # show processed frame
        cv2.imshow('Overlap', overlap_image)
        # press esc to quit
        if cv2.waitKey(1) & 0xFF == 27:
            break
        time.sleep(0.05)
        
    # rrelease vid cap object
    cap.release()
    # destroy opencv windows
    cv2.destroyAllWindows()

# runs first
if __name__ == "__main__":
    import sys
    # if not correct num of arg
    if len(sys.argv) != 2:
        # print message
        print("missing video file argument ( python video.py [video-file] )")
    else:
        # run main
        main(sys.argv[1])