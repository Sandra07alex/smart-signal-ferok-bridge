import cv2
import time

def count_vehicles(image_path):
    # Load the image
    img = cv2.imread(image_path)

    # Preprocess the image (convert to grayscale and apply Gaussian blur)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply binary thresholding (use THRESH_BINARY instead of THRESH_BINARY_INV)
    _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)

    # Detect contours in the thresholded image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter out small contours (optional, depends on image and object size)
    min_contour_area = 1000  # This can be adjusted
    vehicle_count = 0
    for contour in contours:
        if cv2.contourArea(contour) > min_contour_area:
            vehicle_count += 1

    return vehicle_count

def traffic_signal_control():
    while True:
        # Count vehicles on each side (update with valid image paths)
        vehicles_A = count_vehicles("imga.jpg")
        vehicles_B = count_vehicles("imgd.jpg")

        # Determine the traffic signal state
        if vehicles_A == 0:
            print("Side B has green signal.")
        elif vehicles_B == 0:
            print("Side A has green signal.")
        elif vehicles_B > vehicles_A:
            print("Side B has green signal.")
        else:
            print("Side A has green signal.")

        # Simulate the signal duration
        time.sleep(10)  # Wait for 10 seconds

if __name__ == "__main__":
    traffic_signal_control()
