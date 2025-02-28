import cv2
import numpy as np

def compute_disparity(left_image_path, right_image_path):
    # Load images in grayscale
    left_img = cv2.imread(left_image_path, cv2.IMREAD_GRAYSCALE)
    right_img = cv2.imread(right_image_path, cv2.IMREAD_GRAYSCALE)

    # Create StereoBM object and compute disparity map
    stereo = cv2.StereoBM_create(numDisparities=16*4, blockSize=11)
    disparity = stereo.compute(left_img, right_img)

    # Normalize the disparity for better visualization
    disparity_normalized = cv2.normalize(disparity, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
    disparity_normalized = np.uint8(disparity_normalized)
    print(f"Disparity: {disparity}")
    return disparity, disparity_normalized

def estimate_distance(disparity, focal_length, baseline, object_x, object_y, window_size=10):
    # Extract disparity value around the object's estimated position
    disparity_values = disparity[object_y - window_size // 2 : object_y + window_size // 2,
                                 object_x - window_size // 2 : object_x + window_size // 2]

    # Filter out invalid disparity values (-1 or very low)
    valid_disparity_values = disparity_values[disparity_values > 0]
    if len(valid_disparity_values) > 0:
        disparity_avg = np.mean(valid_disparity_values)  # Average valid disparity values
        print(f"Disparity: {disparity_avg}")
        distance = (focal_length * baseline) / disparity_avg  # Depth computation
    else:
        disparity_avg = None
        distance = None

    return distance

if __name__ == "__main__":
    # Define image paths
    left_image_path = "/Users/masonphan/Downloads/stereo/orange_left.jpg"
    right_image_path = "/Users/masonphan/Downloads/stereo/orange_right.jpg"

    # Compute disparity
    disparity, disparity_normalized = compute_disparity(left_image_path, right_image_path)

    # Display the disparity map
    cv2.imshow("Disparity Map", disparity_normalized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Camera parameters
    focal_length = 540  # in pixels
    baseline = 0.1  # in meters

    # Estimated orange position (approximate center of the image)
    object_x = disparity.shape[1] // 2
    object_y = disparity.shape[0] // 2

    # Compute distance
    distance = estimate_distance(disparity, focal_length, baseline, object_x, object_y)

    if distance:
        print(f"Estimated Distance to Object: {distance:.2f} meters")
    else:
        print("Could not compute distance. Ensure disparity is valid.")
