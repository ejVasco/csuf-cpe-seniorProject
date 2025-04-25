from picamera2 import Picamera2, CameraConfiguration
from datetime import datetime
import time

def capture_stereo_images(left_index=0, right_index=1, resolution=(1280, 720)):
    # Initialize left and right camera
    cam_left = Picamera2(camera_num=left_index)
    cam_right = Picamera2(camera_num=right_index)

    config_left = cam_left.create_still_configuration(main={"size": resolution})
    config_right = cam_right.create_still_configuration(main={"size": resolution})

    cam_left.configure(config_left)
    cam_right.configure(config_right)

    cam_left.start()
    cam_right.start()
    time.sleep(5)  # Allow camera sensors to warm up

    left_img = cam_left.capture_array()
    right_img = cam_right.capture_array()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    left_filename = f"left_00.png"
    right_filename = f"right_00.png"

    from PIL import Image
    Image.fromarray(left_img).save(left_filename)
    Image.fromarray(right_img).save(right_filename)

    print(f"Saved left image as {left_filename}")
    print(f"Saved right image as {right_filename}")

    cam_left.close()
    cam_right.close()

if __name__ == "__main__":
    capture_stereo_images()
