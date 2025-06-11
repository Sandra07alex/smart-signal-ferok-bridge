import cv2
import numpy as np
import tkinter as tk
from tkinter import messagebox
import time

# Initialize background subtractor (MOG2 method)
fgbg_A = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=50)
fgbg_B = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=50)

# Frame rate (FPS) of the video
FPS = 30  # Change this value based on your video FPS

# Time window in seconds (7 seconds)
time_window = 7
frame_window = FPS * time_window  # Number of frames in the 7 seconds window


# Function to detect vehicles in the frame using background subtraction and contour detection
def count_vehicles(frame, fgbg):
    # Apply background subtraction to get the foreground mask
    fgmask = fgbg.apply(frame)

    # Apply some noise removal techniques (blurring)
    fgmask = cv2.medianBlur(fgmask, 5)

    # Find contours in the foreground mask
    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours and count vehicles
    vehicle_count = 0
    for contour in contours:
        if cv2.contourArea(contour) > 500:  # Area threshold to filter out noise
            vehicle_count += 1
            # Draw the contour (for visualization purposes)
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draw a rectangle around the vehicle

    return vehicle_count, fgmask  # Return the number of vehicles and the mask


# Function to update the traffic signal based on vehicle counts
def update_traffic_signal():
    global frame_count_A, frame_count_B, vehicles_A_in_window, vehicles_B_in_window, signal_A, signal_B

    # Default signal state initialization
    signal_A = "Red"
    signal_B = "Red"

    # Capture video feed from video files (for side A and B)
    ret_A, frame_A = cap_A.read()
    ret_B, frame_B = cap_B.read()

    if not ret_A or not ret_B:
        messagebox.showerror("Error", "Unable to capture video feed.")
        return

    # Count vehicles on side A and B
    vehicles_A, fgmask_A = count_vehicles(frame_A, fgbg_A)
    vehicles_B, fgmask_B = count_vehicles(frame_B, fgbg_B)

    # Update the total vehicles count in the 7th second window
    vehicles_A_in_window += vehicles_A
    vehicles_B_in_window += vehicles_B

    frame_count_A += 1
    frame_count_B += 1

    # If 7 seconds have passed, update signals based on counts and reset for the next window
    if frame_count_A >= frame_window:
        if vehicles_A_in_window > vehicles_B_in_window:
            signal_A = "Green"
            signal_B = "Red"
        elif vehicles_A_in_window < vehicles_B_in_window:
            signal_A = "Red"
            signal_B = "Green"
        else:
            signal_A = "Green"
            signal_B = "Red"

        # Reset counters for the next 7-second window
        frame_count_A = 0
        vehicles_A_in_window = 0

    if frame_count_B >= frame_window:
        if vehicles_B_in_window > vehicles_A_in_window:
            signal_A = "Red"
            signal_B = "Green"
        elif vehicles_B_in_window < vehicles_A_in_window:
            signal_A = "Green"
            signal_B = "Red"
        else:
            signal_A = "Green"
            signal_B = "Red"

        # Reset counters for the next 7-second window
        frame_count_B = 0
        vehicles_B_in_window = 0

    # Update the GUI signals
    label_A_signal.config(text=f"A Signal: {signal_A}")
    label_B_signal.config(text=f"B Signal: {signal_B}")

    # Display vehicle counts on GUI
    label_A_count.config(text=f"Vehicles on A (last 7s): {vehicles_A_in_window}")
    label_B_count.config(text=f"Vehicles on B (last 7s): {vehicles_B_in_window}")

    # Show the processed frames (optional for debugging)
    cv2.imshow("Side A Vehicle Detection", frame_A)
    cv2.imshow("Side B Vehicle Detection", frame_B)

    # Continue the process by calling the function again after a short delay
    window.after(100, update_traffic_signal)


# Initialize counters for vehicle counts and frame processing
frame_count_A = 0
frame_count_B = 0
vehicles_A_in_window = 0
vehicles_B_in_window = 0

# Initialize signal variables
signal_A = "Red"
signal_B = "Red"

# Initialize GUI
window = tk.Tk()
window.title("Ferook Bridge Traffic Automation")

# Create labels to display vehicle counts
label_A_count = tk.Label(window, text="Vehicles on A (last 7s): 0", font=("Helvetica", 16))
label_A_count.pack(pady=10)
label_B_count = tk.Label(window, text="Vehicles on B (last 7s): 0", font=("Helvetica", 16))
label_B_count.pack(pady=10)

# Create labels to display traffic signal status
label_A_signal = tk.Label(window, text="A Signal: Red", font=("Helvetica", 16))
label_A_signal.pack(pady=10)
label_B_signal = tk.Label(window, text="B Signal: Red", font=("Helvetica", 16))
label_B_signal.pack(pady=10)

# OpenCV Video capture for both sides A and B using video files
cap_A = cv2.VideoCapture("video_a.mp4")  # Path to the video file for side A
cap_B = cv2.VideoCapture("video_b.mp4")  # Path to the video file for side B

if not cap_A.isOpened() or not cap_B.isOpened():
    messagebox.showerror("Error", "Failed to open video stream.")
    window.quit()

# Start the traffic signal update process
update_traffic_signal()

# Start the Tkinter main loop
window.mainloop()

# Release resources when the window is closed
cap_A.release()
cap_B.release()
cv2.destroyAllWindows()
