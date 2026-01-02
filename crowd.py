import cv2 as cv
from ultralytics import YOLO
import numpy as np
import os

#first we need to import the video and then define a class which takes the video and then helps us to analyze the video
classObjects = ["person","bicycle","car","motorcycle"]
def rescale(frame,scale = .5):
    #first we will rescale the frames inside the video and then we will make the analysis of the video
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width,height)
    return cv.resize(frame,dimensions,interpolation = cv.INTER_CUBIC)

cap = cv.VideoCapture("C:/Users/vijay/OneDrive/Concepts/Coding Concepts/14706612_1920_1080_60fps.mp4")

if not cap.isOpened():
    print("Error: Could not open video file. Please check the file path.")
    exit()

print("Video opened successfully!")
model = YOLO("C:/Users/vijay/OneDrive/Concepts/Coding Concepts/YoloWeights/yolov8n.pt")

while cap.isOpened():
    isTrue, frame = cap.read()
    if not isTrue:
        print("End of the Video")
        break
    rescaled_frame = rescale(frame, scale = 0.4)
    results = model(rescaled_frame,stream = True)
    for result in results:
        boxes = result.boxes
        for box in boxes:
            #lets find the coordinates of each boxes
            x,y,w,h = box.xywh[0]
            x,y,w,h = float(x),float(y),float(w),float(h)
            #calcultae the top left and bottom right
            x1 = int(x - w/2)
            y1= int(y - h/2)
            x2 = int(x + w/2)
            y2 = int(y + h/2)
            #now lets draw a rectangle in order to find the people
            confidence = float(box.conf[0])
            cls1 = int(box.cls[0])
            if cls1 == 0:
                cv.rectangle(rescaled_frame,(x1,y1),(x2,y2),(255,0,0),thickness = 1)
                cv.putText(rescaled_frame,f"{classObjects[cls1]} {confidence:.2f}",(max(0,x1), max(20,y1)), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 1)
    cv.imshow("People Video",rescaled_frame)
    if cv.waitKey(10) & 0xFF == ord('d'):
        break
    #now after opening each and every frame we need to detect the people inside the frame and need to count the number of people inside the frame and show it as the output
    #using the yolo model to count the number of people in the frames
cap.release()
cv.destroyAllWindows()
