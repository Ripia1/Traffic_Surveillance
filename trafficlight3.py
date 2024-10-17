import cv2
import numpy as np
from collections import deque

# Constants
FRAME_BUFFER_SIZE = 10  # Number of frames to consider for majority voting
STATE_GREEN = "green"
STATE_YELLOW = "yellow"
STATE_RED = "red"

# Function to get the most frequent color from a buffer
def get_majority_color(buffer):
    return max(set(buffer), key=buffer.count)

# Function to detect the traffic light status
def traffic_light_status(frame, roi_1):
    roiColor = frame[int(roi_1[1]):int(roi_1[1]+roi_1[3]), int(roi_1[0]):int(roi_1[0]+roi_1[2])]
    hsv = cv2.cvtColor(roiColor, cv2.COLOR_BGR2HSV)

    # Define HSV ranges for red, green, yellow
    lower_hsv_red_1 = np.array([0, 100, 100])
    upper_hsv_red_1 = np.array([9, 255, 255])
    lower_hsv_red_2 = np.array([170, 100, 100])
    upper_hsv_red_2 = np.array([180, 255, 255])
    mask_red_1 = cv2.inRange(hsv, lowerb=lower_hsv_red_1, upperb=upper_hsv_red_1)
    mask_red_2 = cv2.inRange(hsv, lowerb=lower_hsv_red_2, upperb=upper_hsv_red_2)
    mask_red = cv2.bitwise_or(mask_red_1, mask_red_2)
    red_blur = cv2.medianBlur(mask_red, 7)

    lower_hsv_green = np.array([35, 100, 100])
    upper_hsv_green = np.array([85, 255, 255])
    mask_green = cv2.inRange(hsv, lowerb=lower_hsv_green, upperb=upper_hsv_green)
    green_blur = cv2.medianBlur(mask_green, 7)

    lower_hsv_yellow = np.array([10, 100, 100])
    upper_hsv_yellow = np.array([34, 255, 255])
    mask_yellow = cv2.inRange(hsv, lowerb=lower_hsv_yellow, upperb=upper_hsv_yellow)
    yellow_blur = cv2.medianBlur(mask_yellow, 7)

    red_color = np.max(red_blur)
    green_color = np.max(green_blur)
    yellow_color = np.max(yellow_blur)

    traffic_status = ""
    if yellow_color == 255:
        traffic_status = "yellow"
    elif green_color == 255:
        traffic_status = "green"
    elif red_color == 255:
        traffic_status = "red"

    return traffic_status

# Initialize buffer and state 
frame_buffer = deque(maxlen=FRAME_BUFFER_SIZE)
current_state = None

# Function to initialize the current state based on initial frames
def initialize_state(frame_buffer):
    if len(frame_buffer) > 0:
        return get_majority_color(frame_buffer)
    return None

# Main function to detect traffic light status
def detect_traffic_signal(frame, roi_1):
    global current_state

    # Get the current traffic light status
    detected_color = traffic_light_status(frame, roi_1)

    # Add detected color to buffer
    frame_buffer.append(detected_color)

    # Initialize the state based on the first few frames
    if current_state is None and len(frame_buffer) == FRAME_BUFFER_SIZE:
        current_state = initialize_state(frame_buffer)

    # Once state is initialized, enforce traffic light sequence: green -> yellow -> red
    if current_state == STATE_GREEN:
        if detected_color in ["yellow", "red"]:
            current_state = STATE_YELLOW
    elif current_state == STATE_YELLOW:
        if detected_color == "red":
            current_state = STATE_RED
    elif current_state == STATE_RED:
        if detected_color == "green":
            current_state = STATE_GREEN

    return current_state