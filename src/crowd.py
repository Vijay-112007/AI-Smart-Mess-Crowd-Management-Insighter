import cv2 as cv
from ultralytics import YOLO
import time
import firebase_admin
from firebase_admin import credentials,db


#first we need to import the video and then define a class which takes the video and then helps us to analyze the video
def resize_to_standard(frame,width = 720,height = 640):
    return cv.resize(frame,(width,height),interpolation = cv.INTER_AREA)
class VideoAnalytics():
    def __init__(self,path,modelpath,firebase_cred_path = None,database_url = None):
        self.path = path
        self.model = YOLO(modelpath)
        self.classNames = self.model.names
        self.maskzone_x1 = None
        self.maskzone_x2 = None
        self.total_count = 0
        self.current_count = 0
        self.suggestion = "Initializing...."
        self.status = "Loading..."
        self.color_code = "Gray"
        self.last_updated_time = ""
        if firebase_cred_path and database_url:
            cred = credentials.Certificate(firebase_cred_path)
            firebase_admin.initialize_app(cred,{'databaseURL':database_url})
    def print_analytics_table(self):
        # Move cursor to top and clear screen
        print("\033[H\033[J", end="")
        # Printing table
        print("-" * 75)
        print(" " * 20 + "🍽️  MESS CROWD ANALYTICS" + " " * 20)
        print("-" * 75)
        print()
        print("🤖 AI SUGGESTION:")
        print(f"     {self.suggestion}")
        print()
        print("-" * 75)
        print()
        print("📊 CROWD ANALYTICS:")
        print(f"     |_ Current Count (Live):  {self.current_count} people")
        print(f"     |_ Total Count (Peak):     {self.total_count} people")
        print(f"     |_ Status:                 {self.status}")
        print(f"     |_ Last Updated:           {self.last_updated_time}")
        print(f"     |_Intensity:               {self.color_code}")
        print()
        print("-" * 75)
        print("\n  Press 'd' on video window to quit", end="", flush=True)
    ##
    def videoanalysis(self):
        cap = cv.VideoCapture(self.path)

        if not cap.isOpened():
            print("Error: Could not open video file. Please check the file path.")
            exit()
        print("Video opened successfully!")
        #adding the time to record

        start_time = time.time()
        last_update = start_time
        last_table_update = start_time

        while cap.isOpened():
            isTrue, frame = cap.read()
            if not isTrue:
                print("End of the Video")
                break
            rescaled_frame = resize_to_standard(frame)
            results = self.model(rescaled_frame,stream = True,verbose = False)
            
            #for counting the people implement this logic
            current_frame_count = 0

            for result in results:
                boxes = result.boxes
                # in order make up the mask area to avoid detection of food servents etc like the cam should be also perfect and changes can be done later
                for box in boxes:
                    cls = int(box.cls[0])
                    conf = box.conf[0] * 100
                    if self.classNames[cls] == 'bowl' or self.classNames[cls] == 'spoon' and conf > 10:
                        x,y,w,h = box.xywh[0]
                        self.maskzone_x1 = int(x-w//2)
                        self.maskzone_x2 = int(x+w//2)
                        #if maskzone is found 
                        break
                for box in boxes: 
                    cls1 = int(box.cls[0])
                    conf = box.conf[0] * 100
                    # If it is a person (class 0)
                    if self.classNames[cls1] == 'person' and conf > 10:
                        current_frame_count += 1 # Increment the count
                        
                        # Get coordinates for drawing
                        x, y, w, h = box.xywh[0]
                        x1 = int(float(x) - float(w)/2)
                        y1 = int(float(y) - float(h)/2)
                        x2 = int(float(x) + float(w)/2)
                        y2 = int(float(y) + float(h)/2)
                        #drawing rectangle for people
                        if self.maskzone_x2 is None or x1 > self.maskzone_x2:
                            cv.rectangle(rescaled_frame,(x1,y1),(x2,y2),(255,0,0),thickness = 1)
                            cv.putText(rescaled_frame,f"{self.classNames[cls1]}",(max(0,x1), max(20,y1)), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 1)
            
            #updates the counts
            self.current_count = current_frame_count
            if current_frame_count > self.total_count:
                self.total_count = current_frame_count
            current_time = time.time()

            #updates the firebase every 5 secondsd
            if current_time - last_update >= 5:
                if current_frame_count > 20:
                    self.suggestion = "Very Crowded! Do not enter."
                    self.status = "Crowded"
                    self.color_code = "red"
                elif current_frame_count > 10:
                    self.suggestion = "Moderately full. You might have to wait."
                    self.status = "Moderate"
                    self.color_code = "orange"
                else:
                    self.suggestion = "Mess is free! Perfect time to eat."
                    self.status = "Available"
                    self.color_code = "green"
                try:
                    ref = db.reference("Mess-System")
                    ref.update({
                        "hall-1":{
                            'name' : "Main Mess",
                            'count': current_frame_count,
                            'status':self.status
                        },
                        'best_suggestion':{
                            'message':self.suggestion,
                            'color':self.color_code
                        },
                        'last_updated':current_time
                    })
                except Exception as e:
                    print("Failed to Update the Data Base")
                self.last_updated_time = time.strftime("%H:%M:%S",time.localtime(current_time))
                last_update = current_time
            if current_time - last_table_update >= 5:
                self.print_analytics_table()
                last_table_update = current_time
            
            cv.putText(rescaled_frame, f"Live Count: {current_frame_count}", (20, 40), 
                      cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            cv.imshow("People Video", rescaled_frame)
            
            if cv.waitKey(1) & 0xFF == ord('d'):
                break
        cap.release()
        cv.destroyAllWindows()
        #Showing the final table
        print("\n\n" + "=" * 75)
        print(" " * 25 + "FINAL ANALYTICS")
        print("=" * 75)
        self.print_analytics_table()
        
        return self.total_count