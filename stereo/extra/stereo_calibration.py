import cv2
import numpy as np
import glob
import os

# === Settings ===
chessboard_size = (9, 6)
square_size = 0.035  # in meters

left_images = sorted(glob.glob("calib_left/*.png"))
right_images = sorted(glob.glob("calib_right/*.png"))

assert len(left_images) == len(right_images), "Mismatch in number of stereo images"

# Prepare object points (0,0,0), (1,0,0), ..., like a chessboard pattern
objp = np.zeros((chessboard_size[0]*chessboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)
objp *= square_size

# Arrays to store points
objpoints = []     # 3D real-world points
imgpointsL = []    # 2D image points for left camera
imgpointsR = []    # 2D image points for right camera

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

for left_path, right_path in zip(left_images, right_images):
    imgL = cv2.imread(left_path)
    imgR = cv2.imread(right_path)
    grayL = cv2.cvtColor(imgL, cv2.COLOR_BGR2GRAY)
    grayR = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)

    foundL, cornersL = cv2.findChessboardCorners(grayL, chessboard_size,None)
    foundR, cornersR = cv2.findChessboardCorners(grayR, chessboard_size,None)

    if foundL and foundR:
        cornersL = cv2.cornerSubPix(grayL, cornersL, (11, 11), (-1, -1), criteria)
        cornersR = cv2.cornerSubPix(grayR, cornersR, (11, 11), (-1, -1), criteria)
        objpoints.append(objp)
        imgpointsL.append(cornersL)
        imgpointsR.append(cornersR)
        
        #cv2.drawChessboardCorners(imgL,chessboard_size,cornersL,foundL)
        #cv2.imshow("left", imgL)
        
        #cv2.drawChessboardCorners(imgR,chessboard_size,cornersR,foundR)
        #cv2.imshow("right", imgR)
        #cv2.waitKey(1000)
cv2.destroyAllWindows()        
print(f"✅ Using {len(objpoints)} valid stereo pairs for calibration")

# Calibrate each camera
retL, mtxL, distL, _, _ = cv2.calibrateCamera(objpoints, imgpointsL, grayL.shape[::-1], None, None)
retR, mtxR, distR, _, _ = cv2.calibrateCamera(objpoints, imgpointsR, grayR.shape[::-1], None, None)

# Stereo calibration
flags = 0
flags |= cv2.CALIB_FIX_INTRINSIC
criteria_stereo = (cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS, 30, 0.001)
retStereo, _, _, _, _, R, T, E, F = cv2.stereoCalibrate(
    objpoints, imgpointsL, imgpointsR,
    mtxL, distL, mtxR, distR, grayL.shape[::-1],
    criteria=criteria_stereo, flags=flags)
print (f"RMS error:", retStereo)   
print (f"Left error: {retL:.4f}")
print (f"Right error: {retR:.4f}")
# Stereo rectification
rectifyScale = 1
R1, R2, P1, P2, Q, _, _ = cv2.stereoRectify(mtxL, distL, mtxR, distR, grayL.shape[::-1], R, T, alpha=0)

map1x,map1y = cv2.initUndistortRectifyMap(mtxL,distL,R1,P1,grayL.shape[::-1],cv2.CV_32FC1)
map2x,map2y = cv2.initUndistortRectifyMap(mtxR,distR,R2,P2,grayR.shape[::-1],cv2.CV_32FC1)
# Save calibration
np.savez("calib.npz", 
         map1x=map1x, map1y= map1y,
         map2x=map2x, map2y= map2y,
         Q=Q)

print("Calibration complete. Saved as calib.npz")


