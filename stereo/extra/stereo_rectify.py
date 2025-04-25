import cv2
import numpy as np

# Load stereo image pair (left and right)
imgL = cv2.imread("1mtestL.png")   # Replace with your own test image
imgR = cv2.imread("1mtestR.png")

# Load rectification maps from saved calibration
calib = np.load("calib.npz")
map1x = calib["map1x"]
map1y = calib["map1y"]
map2x = calib["map2x"]
map2y = calib["map2y"]

# Apply rectification (undistort and align epipolar lines)
imgL_rect = cv2.remap(imgL, map1x, map1y, cv2.INTER_LANCZOS4,cv2.BORDER_CONSTANT)
imgR_rect = cv2.remap(imgR, map2x, map2y, cv2.INTER_LANCZOS4,cv2.BORDER_CONSTANT)

# OPTIONAL: Visualize the result with epipolar lines
stacked = np.hstack((imgL_rect, imgR_rect))
for y in range(0, stacked.shape[0], 40):
    cv2.line(stacked, (0, y), (stacked.shape[1], y), (0, 255, 0), 1)

cv2.imshow("Rectified Pair with Epipolar Lines", stacked)
cv2.waitKey(0)
cv2.destroyAllWindows()

