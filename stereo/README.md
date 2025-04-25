Required Packages: <br/>

OpenCV, Numpy<br/>
sudo apt update<br/>
sudo apt install python3-opencv python3-numpy<br/>

pip install opencv-python numpy<br/>


Picamera2 (raspberry pi only)<br/>
sudo apt update<br/>
sudo apt install -y python3-picamera2<br/>

skLearn<br/>

sudo apt update<br/>
sudo apt install python3-sklearn<br/>

pip install scikit-learn<br/>

Steps:<br/>
1. run picture.py
  - outputs stereo images left_00.png and right_00.png
2. run stereo_depth.oy
  - reads calib.npz, left_00.png and right_00.png
  - outputs diparity and depth at center
3. run slope.py
  - read disparity
