import cv2
import numpy as np
#import matplotlib.pyplot as plt

# Load stereo image pair (left and right)
imgL = cv2.imread("left_00.png")   # Replace with your own test image
imgR = cv2.imread("right_00.png")

# Load rectification maps from saved calibration
calib = np.load("calib.npz")
map1x = calib["map1x"]
map1y = calib["map1y"]
map2x = calib["map2x"]
map2y = calib["map2y"]

# Apply rectification (undistort and align epipolar lines)
imgL_rect = cv2.remap(imgL, map1x, map1y, cv2.INTER_LANCZOS4,cv2.BORDER_CONSTANT)
imgR_rect = cv2.remap(imgR, map2x, map2y, cv2.INTER_LANCZOS4,cv2.BORDER_CONSTANT)
# Convert to grayscale
grayL = cv2.cvtColor(imgL_rect, cv2.COLOR_BGR2GRAY) if imgL.ndim == 3 else imgL
grayR = cv2.cvtColor(imgR_rect, cv2.COLOR_BGR2GRAY) if imgR.ndim == 3 else imgR

width, height = 1280,720
cx = width/2
cy = height/2
fx=924.44
baseline = 0.06
Q1 = np.float32([
   [1,0,0,-cx],
    [0,1,0,-cy],
    [0,0,0,fx],
    [0,0,1.0/baseline,0]
])

Q = calib["Q"]

Q = (Q+Q1)/2.0

# ==== Step 3: Compute disparity map using StereoSGBM ====
stereo = cv2.StereoSGBM_create(
    minDisparity=0,
    numDisparities=16*10,
    blockSize=11,
    P1=8 * 3 * 11**2,
    P2=32 * 3 * 11**2,
    disp12MaxDiff=1,
    uniquenessRatio=10,
    speckleWindowSize=100,
    speckleRange=32,
    preFilterCap=63,
    mode=cv2.STEREO_SGBM_MODE_SGBM_3WAY
)

disparity = stereo.compute(grayL, grayR).astype(np.float32) / 16.0

# ==== Step 4: Convert disparity to 3D coordinates ====
points_3D = cv2.reprojectImageTo3D(disparity, Q)

# Extract depth (Z-coordinate)
depth_map = points_3D[:, :, 2]

# Mask invalid values (disparity <= 0)
depth_map[disparity <= 0] = np.nan

# ==== Step 5: Visualize ====

# Display disparity map
disp_vis = cv2.normalize(disparity, None, 0, 255, cv2.NORM_MINMAX)
disp_vis = np.uint8(disp_vis)
cv2.imshow("Left", imgL_rect)
cv2.imshow("Disparity", disp_vis)
cv2.imwrite("disparity.png",disparity)

# Display depth map using matplotlib
#plt.figure(figsize=(10, 5))
#plt.imshow(depth_map, cmap="plasma")
#plt.colorbar(label="Depth (m)")
#plt.title("Depth Map (Z values)")
#plt.show()

depth_at_center = depth_map[depth_map.shape[0] // 2, depth_map.shape[1]//2]
print(f"depth at center: {depth_at_center: .2f} meters")
cv2.waitKey(0)
cv2.destroyAllWindows()
