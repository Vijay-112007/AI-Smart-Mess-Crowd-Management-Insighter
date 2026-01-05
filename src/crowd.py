import cv2 as cv
from ultralytics import YOLO
import time
import firebase_admin
from firebase_admin import credentials,db


#first we need to import the video and then define a class which takes the video and then helps us to analyze the video
classObjects = ["person","bicycle","car","motorcycle"]
def rescale(frame,scale = .5):
    #first we will rescale the frames inside the video and then we will make the analysis of the video
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width,height)
    return cv.resize(frame,dimensions,interpolation = cv.INTER_CUBIC)
class VideoAnalytics():
    def __init__(self,path,modelpath,firebase_cred_path = None,database_url = None):
        self.path = path
        self.model = YOLO(modelpath)

        if firebase_cred_path and database_url:
            cred = credentials.Certificate(firebase_cred_path)
            firebase_admin.initialize_app(cred,{'databaseURL':database_url})
    
    def videoanalysis(self):
        cap = cv.VideoCapture(self.path)

        if not cap.isOpened():
            print("Error: Could not open video file. Please check the file path.")
            exit()
        print("Video opened successfully!")
        #adding the time to record

        start_time = time.time()
        last_update = start_time

        while cap.isOpened():
            isTrue, frame = cap.read()
            if not isTrue:
                print("End of the Video")
                break
            rescaled_frame = rescale(frame, scale = 0.4)
            results = self.model(rescaled_frame,stream = True,verbose = False)
            
            #for counting the people implement this logic
            current_frame_count = 0

            for result in results:
                boxes = result.boxes
                for box in boxes:
                    cls1 = int(box.cls[0])
                    # If it is a person (class 0)
                    if cls1 == 0:
                        current_frame_count += 1 # Increment the count
                        
                        # Get coordinates for drawing
                        x, y, w, h = box.xywh[0]
                        x1 = int(float(x) - float(w)/2)
                        y1 = int(float(y) - float(h)/2)
                        x2 = int(float(x) + float(w)/2)
                        y2 = int(float(y) + float(h)/2)
                        #drawing rectangle for people
                        cv.rectangle(rescaled_frame,(x1,y1),(x2,y2),(255,0,0),thickness = 1)
                        cv.putText(rescaled_frame,f"{classObjects[cls1]}",(max(0,x1), max(20,y1)), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 1)
            
            #adding the logic
            current_time = time.time()
            if current_time - last_update >= 5:
                #logic for status and color
                suggestion = ""
                status = ""
                color_code = ""

                if current_frame_count > 45:
                    suggestion = "Very Crowded! Do not enter."
                    status = "Crowded"
                    color_code = "red"
                elif current_frame_count > 25:
                    suggestion = "Moderately full. You might have to wait."
                    status = "Moderate"
                    color_code = "orange"
                else:
                    suggestion = "Mess is free! Perfect time to eat."
                    status = "Available"
                    color_code = "green"
                # Update Firebase
                try:
                    ref = db.reference('mess_system')
                    ref.update({
                        'hall_1': {
                            'name': 'Main Mess',
                            'count': current_frame_count,
                            'status': status
                        },
                        'best_suggestion': {
                            'message': suggestion,
                            'color': color_code
                        },
                        'last_updated': current_time
                    })
                    print(f"📡 Firebase Updated | Count: {current_frame_count} | {status}")
                except Exception as e:
                    print(f"Firebase Error: {e}")

                last_update = current_time

            # Show the real-time count on the screen
            cv.putText(rescaled_frame, f"Live Count: {current_frame_count}", (20, 40), 
                       cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            cv.imshow("People Video", rescaled_frame)
            
            # Press 'd' to quit
            if cv.waitKey(1) & 0xFF == ord('d'):
                break
            #now after opening each and every frame we need to detect the people inside the frame and need to count the number of people inside the frame and show it as the output
            #using the yolo model to count the number of people in the frames
        cap.release()
        cv.destroyAllWindows()
        return current_frame_count