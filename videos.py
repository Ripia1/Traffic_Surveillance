import cv2
import numpy as np
import glob

img_array = []

images = glob.glob('/Users/richardpianimjr/Yolov8-2/images/*.jpg')
# for image in sorted(images):
#     print(image)


for filename in sorted(images):
    print(filename)
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)
   
out = cv2.VideoWriter('cropped_video2.mp4',cv2.VideoWriter_fourcc(*'DIVX'), 10, size)

for i in range(len(img_array)):
   out.write(img_array[i])
out.release()