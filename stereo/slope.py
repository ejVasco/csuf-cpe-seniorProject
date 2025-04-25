import cv2
import numpy as np
from sklearn.linear_model import RANSACRegressor

def estimate_slope_from_depth(depth_map, fx, fy, cx, cy):
    h, w = depth_map.shape

    # Create meshgrid of pixel coordinates
    i, j = np.meshgrid(np.arange(w), np.arange(h))  # i = x, j = y

    Z = depth_map.flatten()
    X = ((i.flatten() - cx) * Z) / fx
    Y = ((j.flatten() - cy) * Z) / fy

    # Mask invalid values
    valid = ~np.isnan(Z) & ~np.isinf(Z)
    X, Y, Z = X[valid], Y[valid], Z[valid]

    # Fit a plane Z = aX + bY + c using RANSAC
    A = np.column_stack((X, Y))
    ransac = RANSACRegressor().fit(A, Z)
    a, b = ransac.estimator_.coef_

    # Normal vector of the plane is [-a, -b, 1]
    normal = np.array([-a, -b, 1])
    normal = normal / np.linalg.norm(normal)

    # Slope = angle between normal and vertical axis
    vertical = np.array([0, 0, 1])
    angle_rad = np.arccos(np.dot(normal, vertical))
    slope_deg = np.degrees(angle_rad)
    return slope_deg

# === Load disparity map and Q matrix ===
disparity = cv2.imread("disparity.png", cv2.IMREAD_UNCHANGED).astype(np.float32) / 16.0
calib = np.load("calib.npz")

width, height = 1280,720
cx = width/2
cy = height/2
fx=924.44
fy=924.44
baseline = 0.06
Q1 = np.float32([
   [1,0,0,-cx],
    [0,1,0,-cy],
    [0,0,0,fx],
    [0,0,1.0/baseline,0]
])

Q = calib["Q"]

Q = (Q+Q1)/2.0
# Reproject to 3D and extract depth (Z)
points_3D = cv2.reprojectImageTo3D(disparity, Q)
depth_map = points_3D[:, :, 2]
depth_map[disparity <= 0] = np.nan

# === Camera intrinsics (replace if different) ===
#fx = 1.25e3  # focal length in pixels
#fy = 1.25e3

# === Estimate Slope ===
slope = estimate_slope_from_depth(depth_map, fx, fy, cx, cy)
print(f"Estimated surface slope: {slope:.2f} degrees")
