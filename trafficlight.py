import cv2
import numpy as np

def traffic_light_status(frame, traffic_signal_roi):
    
    roiColor= frame[int(traffic_signal_roi[1]):int(traffic_signal_roi[1]+traffic_signal_roi[3]), int(traffic_signal_roi[0]):int(traffic_signal_roi[0]+traffic_signal_roi[2])]
   
    hsv = cv2.cvtColor(roiColor, cv2.COLOR_BGR2HSV)    
        #red
    lower_hsv_red = np.array([157,177,122])
    upper_hsv_red = np.array([179,255,255])
    mask_red = cv2.inRange(hsv,lowerb=lower_hsv_red,upperb=upper_hsv_red)
        #Median filtering
    red_blur = cv2.medianBlur(mask_red, 7)
        #green
    lower_hsv_green = np.array([49,79,137])
    upper_hsv_green = np.array([90,255,255])
    mask_green = cv2.inRange(hsv,lowerb=lower_hsv_green,upperb=upper_hsv_green)
        #Median filtering
    green_blur = cv2.medianBlur(mask_green, 7)
        #Because the image is a binary image, so if the image has a white point, which is 255, then take his maximum value of 255
    red_color = np.max(red_blur)
    green_color = np.max(green_blur)
        #Judging the binary image in red_color if the value is equal to 255, then it is judged as red
    if red_color == 255:
        traffic_signal = 'red'
        #Judge the binary image in green_color if the value is equal to 255, then judge it as green
    elif green_color == 255:
        traffic_signal = 'green' 
    
    return traffic_signal