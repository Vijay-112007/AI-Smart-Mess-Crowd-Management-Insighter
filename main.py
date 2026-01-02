from authentication import Authentication,SignIn,SignUp
import math
import numpy as np
import cv2 as cv
from crowd import VideoAnalytics
import time
def main():
    #first we will ask either to sign up or sign in
    choice = int(input("1. Sign Up \n 2. Login In \n Enter Your Choice: "))
    if choice == 1:
        choice1 = int(input("1.Sign Up as Admin\n2.Sign Up as User\nEnter Your Choice: "))
        if choice1 == 1:
            newadmin = SignUp(input("Enter Your New Username:"),input("Enter Your New Password: "),input("Enter Your Email:"))
            print("Signing In......")
            time.sleep(10)
            print(newadmin.sign_in())
            #we need to provide three options after login into the system
            print("1. Crowd Analytics\n2.Scan the QR\n3.Food Insights")
            choice2 = input("Enter Your Choice: ")
            match(choice2):
                case "1":
                    va1 = VideoAnalytics("C:/Users/vijay/OneDrive/Concepts/Coding Concepts/14706612_1920_1080_60fps.mp4","C:/Users/vijay/OneDrive/Concepts/Coding Concepts/YoloWeights/yolov8n.pt")
                    print("Press \"D\" to Stop the Video")
                    va1.videoanalysis()
                    print("Video Successfully Ended")
    elif choice == 2:
        choice1 = int(input("1.Sign In as Admin\n2.Sign In as User\nEnter Your Choice: "))
        if choice1 == 1:
            newadmin = SignIn(input("Enter Your Username: "),input("Enter Your Password: "))
            print("Signing In......")
            time.sleep(10)
            print(newadmin.sign_in())
            #we need to provide three options after login into the system
            print("1. Crowd Analytics\n2.Scan the QR\n3.Food Insights")
            choice2 = input("Enter Your Choice: ")
            match(choice2):
                case "1":
                    va1 = VideoAnalytics("C:/Users/vijay/OneDrive/Concepts/Coding Concepts/14706612_1920_1080_60fps.mp4","C:/Users/vijay/OneDrive/Concepts/Coding Concepts/YoloWeights/yolov8n.pt")
                    print("Press \"D\" to Stop the Video")
                    va1.videoanalysis()
                    print("Video Successfully Ended")
    pass
if __name__ == "__main__":
    main()