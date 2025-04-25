import cv2
import numpy as np
from picamera2 import Picamera2
import threading
import os

# === Settings ===
chessboard_size = (9, 6)  # inner corners
square_size = 0.035       # optional (in meters)

os.makedirs("calib_left", exist_ok=True)
os.makedirs("calib_right", exist_ok=True)

# === Init cameras ===
picam0 = Picamera2(0)
picam1 = Picamera2(1)
config0 = picam0.create_preview_configuration(main={"format": "RGB888", "size": (1280, 720)})
config1 = picam1.create_preview_configuration(main={"format": "RGB888", "size": (1280, 720)})
picam0.configure(config0)
picam1.configure(config1)

frames = {}
running = True

def stream(picam, key):
    picam.start()
    while running:
        frames[key] = picam.capture_array()

thread0 = threading.Thread(target=stream, args=(picam0, "left"))
thread1 = threading.Thread(target=stream, args=(picam1, "right"))
thread0.start()
thread1.start()

# === Live viewer ===
img_id = 0
print("Press 's' to save a stereo pair (if corners detected)")
print("Press 'q' to quit")

while True:
    if "left" in frames and "right" in frames:
        grayL = cv2.cvtColor(frames["left"], cv2.COLOR_BGR2GRAY)
        grayR = cv2.cvtColor(frames["right"], cv2.COLOR_BGR2GRAY)

        foundL, cornersL = cv2.findChessboardCorners(grayL, chessboard_size)
        foundR, cornersR = cv2.findChessboardCorners(grayR, chessboard_size)

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        if foundL:
            cornersL = cv2.cornerSubPix(grayL, cornersL, (11,11), (-1,-1), criteria)
        if foundR:
            cornersR = cv2.cornerSubPix(grayR, cornersR, (11,11), (-1,-1), criteria)

        visL = frames["left"].copy()
        visR = frames["right"].copy()

        if foundL:
            cv2.drawChessboardCorners(visL, chessboard_size, cornersL, foundL)
        if foundR:
            cv2.drawChessboardCorners(visR, chessboard_size, cornersR, foundR)

        stacked = np.hstack((visL, visR))
        cv2.imshow("Live Stereo Calibration Viewer", stacked)

        key = cv2.waitKey(1)
        if key == ord('s') and foundL and foundR:
            cv2.imwrite(f"calib_left/left_{img_id:02d}.png", frames["left"])
            cv2.imwrite(f"calib_right/right_{img_id:02d}.png", frames["right"])

            print(f"✅ Saved pair #{img_id}")
            img_id += 1
        elif key == ord('q'):
            break

cv2.destroyAllWindows()
running = False
thread0.join()
thread1.join()
picam0.stop()
picam1.stop()


