import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
import csv, os
from datetime import datetime
from sklearn.linear_model import RANSACRegressor

class StereoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stereo Depth Analyzer")
        self.root.geometry("500x300")

        self.left_image_path = None
        self.right_image_path = None

        tk.Label(root, text="Stereo Depth Analysis GUI", font=("Helvetica", 16, "bold")).pack(pady=10)

        tk.Button(root, text="Load Left Image", command=self.load_left).pack(pady=5)
        tk.Button(root, text="Load Right Image", command=self.load_right).pack(pady=5)
        tk.Button(root, text="Run Analysis", command=self.run_analysis).pack(pady=20)

        self.status = tk.Label(root, text="🟡 Waiting for image input...", fg="blue")
        self.status.pack(pady=10)

    def load_left(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
        if path:
            self.left_image_path = path
            self.status.config(text=f"✅ Left image loaded.")
    
    def load_right(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
        if path:
            self.right_image_path = path
            self.status.config(text=f"✅ Right image loaded.")

    def run_analysis(self):
        if not self.left_image_path or not self.right_image_path:
            messagebox.showerror("Missing Input", "Please load both left and right images.")
            return
        
        try:
            self.process_images(self.left_image_path, self.right_image_path)
            self.status.config(text="✅ Analysis complete and written to CSV.", fg="green")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def process_images(self, left_path, right_path):
        imgL = cv2.imread(left_path)
        imgR = cv2.imread(right_path)

        calib = np.load("calib.npz")
        map1x = calib["map1x"]
        map1y = calib["map1y"]
        map2x = calib["map2x"]
        map2y = calib["map2y"]
        Q = calib["Q"]

        imgL_rect = cv2.remap(imgL, map1x, map1y, cv2.INTER_LANCZOS4)
        imgR_rect = cv2.remap(imgR, map2x, map2y, cv2.INTER_LANCZOS4)

        grayL = cv2.cvtColor(imgL_rect, cv2.COLOR_BGR2GRAY)
        grayR = cv2.cvtColor(imgR_rect, cv2.COLOR_BGR2GRAY)

        # Camera params
        width, height = 1280, 720
        cx = width / 2
        cy = height / 2
        fx = fy = 924.44
        baseline = 0.06

        Q1 = np.float32([
            [1, 0, 0, -cx],
            [0, 1, 0, -cy],
            [0, 0, 0, fx],
            [0, 0, 1.0 / baseline, 0]
        ])
        Q = (Q + Q1) / 2.0

        stereo = cv2.StereoSGBM_create(
            minDisparity=0,
            numDisparities=16 * 10,
            blockSize=11,
            P1=8 * 3 * 11 ** 2,
            P2=32 * 3 * 11 ** 2,
            disp12MaxDiff=1,
            uniquenessRatio=10,
            speckleWindowSize=100,
            speckleRange=32,
            preFilterCap=63,
            mode=cv2.STEREO_SGBM_MODE_SGBM_3WAY
        )

        disparity = stereo.compute(grayL, grayR).astype(np.float32) / 16.0
        points_3D = cv2.reprojectImageTo3D(disparity, Q)
        depth_map = points_3D[:, :, 2]
        depth_map[disparity <= 0] = np.nan

        def estimate_slope_from_depth(depth_map, fx, fy, cx, cy):
            h, w = depth_map.shape
            i, j = np.meshgrid(np.arange(w), np.arange(h))
            Z = depth_map.flatten()
            X = ((i.flatten() - cx) * Z) / fx
            Y = ((j.flatten() - cy) * Z) / fy
            valid = ~np.isnan(Z) & ~np.isinf(Z)
            X, Y, Z = X[valid], Y[valid], Z[valid]
            A = np.column_stack((X, Y))
            ransac = RANSACRegressor().fit(A, Z)
            a, b = ransac.estimator_.coef_
            normal = np.array([-a, -b, 1])
            normal /= np.linalg.norm(normal)
            angle_rad = np.arccos(np.dot(normal, np.array([0, 0, 1])))
            return np.degrees(angle_rad)

        center_depth = depth_map[depth_map.shape[0] // 2, depth_map.shape[1] // 2]
        slope = estimate_slope_from_depth(depth_map, fx, fy, cx, cy)

        print(f"Depth at center: {center_depth:.2f} m")
        print(f"Estimated slope: {slope:.2f} degrees")

        # Save to CSV
        filename = "landslide_data.csv"
        file_exists = os.path.isfile(filename)
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Timestamp", "Depth (m)", "Slope (deg)"])
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), f"{center_depth:.2f}", f"{slope:.2f}"])

        # Display for confirmation
        #disp_vis = cv2.normalize(disparity, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        #cv2.imshow("Disparity Map", disp_vis)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()


# Start GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = StereoApp(root)
    root.mainloop()
