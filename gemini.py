import cv2
import time
import torch

# Load a pre-trained object detection model (e.g., YOLOv8)
model = torch.hub.load('ultralytics/yolov8', 'yolov8n')

def detect_vehicles(image):
    results = model(image)
    df = results.pandas().xyxy[0]
    vehicle_classes = ['car', 'truck', 'bus', 'motorcycle', 'bicycle']
    vehicle_count = df[df['name'].isin(vehicle_classes)].shape[0]
    return vehicle_count

def set_traffic_lights(side_A_priority):
    # Replace this with actual hardware control (e.g., GPIO pins, relays)
    if side_A_priority:
        print("Green for A, Red for B")
    else:
        print("Red for A, Green for B")

# Read the videos
cap_A = cv2.VideoCapture('video_A.mp4')
cap_B = cv2.VideoCapture('video_B.mp4')

while True:
    ret_A, frame_A = cap_A.read()
    ret_B, frame_B = cap_B.read()

    if not ret_A or not ret_B:
        break

    # Detect vehicles in each image
    count_A = detect_vehicles(frame_A)
    count_B = detect_vehicles(frame_B)

    # Determine the side with priority
    if count_A > count_B:
        set_traffic_lights(True)  # Prioritize side A
    elif count_B > count_A:
        set_traffic_lights(False)  # Prioritize side B
    else:
        # Alternate between sides (e.g., using a timer or random selection)
        set_traffic_lights(True)  # Prioritize side A for this cycle
        time.sleep(5)
        set_traffic_lights(False)  # Prioritize side B for the next cycle

    # Display the frames (optional)aa
    cv2.imshow('Frame A', frame_A)
    cv2.imshow('Frame B', frame_B)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap_A.release()
cap_B.release()
cv2.destroyAllWindows()