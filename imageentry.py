import cv2
import time

def count_vehicles(image_path):
    # Load the image
    img = cv2.imread(image_path)

    # Preprocess the image (e.g., convert to grayscale, apply thresholding)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

    # Detect vehicles (e.g., using contour detection)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Count the number of detected vehicles
    vehicle_count = len(contours)

    return vehicle_count

def traffic_signal_control():
    while True:
        # Count vehicles on each side
        vehicles_A = count_vehicles("imga.jpg")
        vehicles_B = count_vehicles("imgb.jpg")

        # Determine the traffic signal state
        if vehicles_A == 0:
            print("Side B has green signal.")
        elif vehicles_B == 0:
            print("Side A has green signal.")
        elif vehicles_B > vehicles_A:
            print("Side B has green signal.")
        else:
            print("Side A has green signal.")

        # You can add a delay here to simulate the signal duration
        time.sleep(10)  # Wait for 10 seconds

if __name__ == "__main__":
    traffic_signal_control()