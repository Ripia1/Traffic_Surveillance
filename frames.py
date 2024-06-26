# Program To Read video 
# and Extract Frames 

import cv2 

# Function to extract frames 
def FrameCapture(path): 

	# Path to video file 
	vidObj = cv2.VideoCapture(path) 

	# Used as counter variable 
	count = 0

	# checks whether frames were extracted 
	success = 1

	while success: 

		# vidObj object calls read 
		# function extract frames 
		success, image = vidObj.read() 

		if count > 10429 and count < 10524:

		# Saves the frames with frame-count 
			cv2.imwrite("/Users/richardpianimjr/Yolov8-2/images/frame%d.jpg" % count, image) 
  

		count += 1
		if count ==10525:
			break
		print(count)


# Driver Code 
if __name__ == '__main__': 

	# Calling the function 
	FrameCapture("/Users/richardpianimjr/Yolov8-2/video/2019_0509_060031_031A.MP4") 
