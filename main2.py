from ultralytics import YOLO
from collections import defaultdict
import cv2 
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import trafficlight
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import time
import cordinate
#import pytesseract
#from color_recognition_module import color_recognition_api

#Load Yolov8 model
model = YOLO("yolov8n.pt")


#Load video
video_path = '//Users/richardpianimjr/Yolov8-2/cropped_video2.mp4' 
cap = cv2.VideoCapture(video_path)

ret = True
#frame_num = 0
first_frame = True

# Store the track history
track_history = defaultdict(lambda: [])

# Initialize a DataFrame to store the data
df = pd.DataFrame(columns=['frame_number', 'time','object_class', 'tracker_id','traffic_signal', 'jaywalking', 'violation'])
df_main = pd.DataFrame(columns=['frame_number', 'time', 'tracker_id', 'box'])
df_object = pd.DataFrame(columns = ['tracker_id','object_class'])
df_jaywalking = pd.DataFrame(columns=['tracker_id'])
df_red_light_violation = pd.DataFrame(columns=['tracker_id'])

start_time_seconds = 6 * 3600 + 17 * 60 + 50

frame_num = 0

# Read Frames
while ret:
    ret, frame = cap.read()
    
    if ret:
        #Traffic Light Selection
        
        if first_frame: 
            traffic_signal_roi = cv2.selectROI(frame) # traffic light
            crosswalk_bottom_roi = cv2.selectROI(frame) #down crosswalk
            crosswalk_up_roi = cv2.selectROI(frame) #top crosswalk
            crosswalk_left_roi = cv2.selectROI(frame) #left crosswalk
            crosswalk_right_roi = cv2.selectROI(frame) #right crosswalk
            
            
            first_frame = False 
        
        
        
        traffic_signal = trafficlight.traffic_light_status(frame,traffic_signal_roi)
        
        # y1_2 = int(crosswalk_bottom_roi[1])
        # y2_2 = int(crosswalk_bottom_roi[1] +  crosswalk_bottom_roi[3])
        # x1_1 = int(crosswalk_bottom_roi[0])
        # x2_2 = int(crosswalk_bottom_roi[0] + crosswalk_bottom_roi[2])
        
        
        
        #crossing coord bottom
        yb1 = int(crosswalk_bottom_roi[1])
        yb2 = int(crosswalk_bottom_roi[1]+ crosswalk_bottom_roi[3])
        xb1 = int(crosswalk_bottom_roi[0])
        xb2 = int(crosswalk_bottom_roi[0]+ crosswalk_bottom_roi[2])
        #midwalk coordinates
        yc1 = int(crosswalk_up_roi[1])
        yc2 = int(crosswalk_up_roi[1]+ crosswalk_up_roi[3])
        xc1 = int(crosswalk_up_roi[0])
        xc2 = int(crosswalk_up_roi[0]+ crosswalk_up_roi[2])
        #left coordinates
        yd1 = int(crosswalk_left_roi[1])
        yd2 = int(crosswalk_left_roi[1]+ crosswalk_left_roi[3])
        xd1 = int(crosswalk_left_roi[0])
        xd2 = int(crosswalk_left_roi[0]+ crosswalk_left_roi[2])
        #right crosswalk coordinates
        ye1 = int(crosswalk_right_roi[1])
        ye2 = int(crosswalk_right_roi[1]+ crosswalk_right_roi[3])
        xe1 = int(crosswalk_right_roi[0])
        xe2 = int(crosswalk_right_roi[0]+ crosswalk_right_roi[2])            
        
        
        print(yb1, yb2, xb1, xb2)    
   
        
        #Detect objects
        #Track objects
        results = model.track(frame, persist = True)

        #Plot results
        frame_ = results[0].plot()

        # # Get the boxes and track IDs
        # boxes = results[0].boxes.xywh.cpu()
        # trackid =  results[0].boxes.id
        # if trackid is not None:
        #     track_ids = trackid.int().cpu.tolist()
        # class_names = results[0].names
        # classid = results[0].boxes.cls.cpu()
        
        
        
        # Get the boxes and track IDs
        boxes = results[0].boxes.xywh.cpu()
        if results[0].boxes.id is not None:
            track_ids = results[0].boxes.id.int().cpu().tolist()
        class_names = results[0].names
        classid = results[0].boxes.cls.cpu()
        
        

        # Run a for loop for each detected object with their tracking id, bounding box, and object class information
        for box, track_id, classes in zip(boxes, track_ids, classid):
            x, y, w, h = box
            track = track_history[track_id]
            class_name = class_names[int (classes)]
            
            print (track_id, class_name, x, y)

            #Iniatilize Jaywalking
            jay_status = "NA"
            violation = "NA"
            
            #Jaywalking
            if class_name  == 'person':
                if y >= yb1 and y <= yb2:
                    if x >= xb1 and x <= xb2:
                        if traffic_signal == 'green':
                            jay_status = "Jaywalking"
                        if traffic_signal == 'red':
                            jay_status = "Not Jaywalking"
                        cv2.putText(frame_, jay_status,(int(x), int(y)),0, 0.75, (255,255,255),2)
                   

            if class_name  == 'person':
                if y >= yc1 and y <= yc2:
                    if x >= xc1 and x <= xc2:
                        if traffic_signal == 'green':
                            jay_status = "Jaywalking"
                        if traffic_signal == 'red':
                            jay_status = "Not Jaywalking"
                        cv2.putText(frame_, jay_status,(int(x), int(y)),0, 0.75, (255,255,255),2)
                    else:
                        jay_status = "NA"

            if class_name  == 'person':
                if y >= yd1 and y <= yd2:
                    if x >= xd1 and x <= xd2:
                        if traffic_signal == 'green':
                            jay_status = "Not Jaywalking"
                        if traffic_signal == 'red':
                            jay_status = "Jaywalking"
                        cv2.putText(frame_, jay_status,(int(x), int(y)),0, 0.75, (255,255,255),2)
                    else:
                        jay_status = "NA"

            if class_name  == 'person':
                if y >= ye1 and y <= ye2:
                    if x >= xe1 and x <= xe2:
                        if traffic_signal == 'green':
                            jay_status = "Not Jaywalking"
                        if  traffic_signal == 'red':
                            jay_status = "Jaywalking"
                        cv2.putText(frame_, jay_status,(int(x), int(y)),0, 0.75, (255,255,255),2)
                    else:
                        jay_status = "NA"
        
            #Red Light Violation
            if class_name == 'car':
                if y >= yc1 and y <= yc2:
                    if x >= xc1 and x <= xc2:
                        if traffic_signal == 'red':
                            violation = 'Red Light Violation'
                        if traffic_signal == 'green':
                            violation = 'No Red Light Violation'
                        cv2.putText(frame_, violation,(int(x), int(y)),0, 0.75, (255,255,255),2)
                    else:
                        violation  = 'NA'
                        
                        
            #if jay_status == 'Jaywalking' and 
            # Calculate the timestamp based on the frame number
            timestamp = start_time_seconds + (frame_num / 10.0) # 10 frames per second
            timestamp_formatted = time.strftime("%H:%M:%S", time.gmtime(timestamp))
            print(f"Frame {frame_num + 1}: Timestamp {timestamp_formatted} seconds")
            
            traffic_surviellance = {
                'frame_number': frame_num,
                'time': timestamp,
                'object_class': class_name,
                'tracker_id': track_id,
                'box_x': f"{x}",
                'box_y': f"{y}",
                'traffic_signal': traffic_signal,
                'jaywalking': jay_status,
                'violation': violation
            }
            
            main_row = {'frame_number': frame_num,
                           'time': timestamp, 
                           'tracker_id': track_id,
                           'box': f"{x}, {y}"
            }
            
            object = {
                'tracker_id': track_id,
                'object_class': class_name
            }
            
            jaywalking = {
                'tracker_id': track_id
            #     'start_frame': 
            #     'end_frame': 
             }
            
            red_light_violation = {
                 'tracker_id': track_id
            #     'start_frame': 
            #     'end_frame': 
            }
            
            # Append the new row to the DataFrame
            df = pd.concat([df, pd.DataFrame([traffic_surviellance])], ignore_index=True)
         
            df_main = pd.concat([df_main, pd.DataFrame([main_row])], ignore_index=True)
            
            df_object  = pd.concat([df_object, pd.DataFrame([object])],ignore_index=True)
            
            df_jaywalking = pd.concat([df_jaywalking, pd.DataFrame([jaywalking])], ignore_index=True)
            
            df_red_light_violation = pd.concat([df_red_light_violation, pd.DataFrame([red_light_violation])], ignore_index= True)

        
              

        cv2.rectangle(frame_, (int(traffic_signal_roi[0]),int(traffic_signal_roi[1])), (int(traffic_signal_roi[0]+traffic_signal_roi[2]),int(traffic_signal_roi[1]+traffic_signal_roi[3])), (0,0,255), 2)
        cv2.putText(frame_, traffic_signal, (int(traffic_signal_roi[0]-15), int(traffic_signal_roi[1]-10)),0, 0.5, (255,255,255),2)

        

            
        cv2.imshow('frame', frame_)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break        
    
        #NEW VARIABLE
        frame_num += 1
        

cap.release()
cv2.destroyAllWindows()

#Connect Database
# mydb = mysql.connector.connect(
#   host="localhost",
#   user ="root",
#   password ="pianim12345",
#   database="Traffic_Data"
# )


# Database connection details
db_host = '127.0.0.1'
db_user = 'root'
db_password = 'pianim12345'
db_name = 'Traffic_Data'

# Create SQLAlchemy engine
engine = create_engine(f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}")

# Store DataFrame in MySQL database
table_name_traffic_surviellance = 'Traffic_Surviellance'
df.to_sql(table_name_traffic_surviellance, con=engine, if_exists='replace', index=False)

# Store second DataFrame (main) in MySQL database
table_name_main = 'Main'
df_main.to_sql(table_name_main, con=engine, if_exists='replace', index=False)

#Store third DataFrame (object) in MySQL database
table_name_object = 'Object'
df_object.to_sql(table_name_object, con=engine, if_exists='replace', index=False)

#Store fourth DataFrame (jaywalking) in MySQL database
table_name_jaywalking = 'Jaywalking'
df_jaywalking.to_sql(table_name_jaywalking, con=engine, if_exists='replace', index=False)

#Store fifth DataFrame (red_light_violation) in MySQL database
table_name_red_light_violation ='Red Light Violation'
df_red_light_violation.to_sql(table_name_red_light_violation, con=engine, if_exists='replace', index = False)

# Confirm data insertion
print(f"\nDataFrame stored in MySQL table '{table_name_traffic_surviellance}' successfully.")
print(f"Main DataFrame stored in MySQL table '{table_name_main}' successfully.")
print(f"Object DataFrame stored in MySQL table '{table_name_object}' successfully.")
print(f"Jaywalking DataFrame stored in MySQL table '{table_name_jaywalking}' successfully.")
print(f"Red Light Violation stored in MySQL table '{table_name_red_light_violation}' successfully.")

# Save the DataFrame to a CSV file
#df.to_csv('traffic_data.csv', index=False)
    
    # data = {"frame": frame_num,
    #                 "time":time.time(),
    #                 "traffic_signal": = traffic_signal,
    #                 "object": class_name,
    #                 "jaywalking": jay_status,
    #                 "tracker id": track.track_id, }