from src.authentication import SignIn,SignUp
from src.crowd import VideoAnalytics
import time
import os


def main():
    #first we will ask either to sign up or sign in
    currentdir = os.getcwd()
    choice = int(input("1. Sign Up\n2. Login In\nEnter Your Choice: "))
    if choice == 1:
        choice1 = int(input("1.Sign Up as Admin\n2.Sign Up as User\nEnter Your Choice: "))
        if choice1 == 2:
            newuser = SignUp(input("Enter Your New Username:"),input("Enter Your New Password: "),input("Enter Your Email:"),0)
            print("Signing In......")
            print(newuser.sign_in())
            #we need to provide three options after login into the system
            print("1. Crowd Analytics\n2.Scan the QR\n3.Food Insights")
            choice2 = input("Enter Your Choice: ")
            match(choice2):
                case "1":
                    va1 = VideoAnalytics(currentdir + "/assets/Dining_Hall_Queue_Video_Generation.mp4",
                                        currentdir + "/assets/yolov8n.pt",
                                        "newrulesimportant.json",
                                        "https://mess-management-system-1f313-default-rtdb.firebaseio.com/")
                    print("Press \"D\" to Stop the Video")
                    count = va1.videoanalysis()
                    print("Video Successfully Ended")
                case "2":
                    print("Coming Soon....")
                    time.sleep(2)
                case "3":
                    print("Coming Soon....")
                    time.sleep(2)
        elif choice1 == 1:
            newadmin = SignUp(input("Enter Your New Username:"),input("Enter Your New Password: "),input("Enter Your Email:"))
            print("Signing In......")
            print(newadmin.sign_in())
            #we need to provide three options after login into the system
            print("1.Crowd Analytics\n2.Start Generating QR code\n3.Food Insights\n4. Monthly Insights")
            choice2 = input("Enter Your Choice: ")
            match(choice2):
                case "1":
                    va1 = VideoAnalytics(currentdir + "/assets/Dining_Hall_Queue_Video_Generation.mp4",
                                        currentdir + "/assets/yolov8n.pt",
                                        "newrulesimportant.json",
                                        "https://mess-management-system-1f313-default-rtdb.firebaseio.com/")
                    print("Press \"D\" to Stop the Video")
                    print("Loading the Analytics....")
                    count = va1.videoanalysis()
                    time.sleep(3)
                    print("Video Successfully Ended")
                case "2":
                    print("Coming Soon....")
                    time.sleep(2)
                case "3":
                    print("Coming Soon....")
                    time.sleep(2)
    elif choice == 2:
        choice1 = int(input("1.Sign In as Admin\n2.Sign In as User\nEnter Your Choice: "))
        if choice1 == 1:
            newadmin = SignIn(input("Enter Your Username: "),input("Enter Your Password: "))
            print("Signing In......")
            print(newadmin.sign_in())
            newadmin.authenticated = True
            #we need to provide three options after login into the system
            print("1. Crowd Analytics\n2.Start Generating QR code\n3.Food Insights\n4. Monthly Insights\n5.Exit")
            choice2 = input("Enter Your Choice: ")
            match(choice2):
                case "1":
                    va1 = VideoAnalytics(currentdir + "/assets/Dining_Hall_Queue_Video_Generation.mp4",
                                        currentdir + "/assets/yolov8n.pt",
                                        "newrulesimportant.json",
                                        "https://mess-management-system-1f313-default-rtdb.firebaseio.com/")
                    print("Press \"D\" to Stop the Video")
                    print("Loading the Analytics....")
                    va1.videoanalysis()
                    time.sleep(3)
                    print("Video Successfully Ended")
                case "2":
                    print("Coming Soon....")
                    time.sleep(2)
                case "3":
                    print("Coming Soon....")
                    time.sleep(2)
                case "4":
                    print("Coming Soon....")
                    time.sleep(2)
                case "5":
                    newadmin.authenticated = False
        elif choice1 == 2:
            newuser = SignIn(input("Enter Your Username:"),input("Enter Your Password: "),0)
            print("Signing In......")
            print(newuser.sign_in())
            #we need to provide three options after login into the system
            print("1. Crowd Analytics\n2.Scan the QR\n3.Food Insights\n4.Exit")
            newuser.authenticated = True
            choice2 = input("Enter Your Choice: ")
            match(choice2):
                case "1":
                    va1 = VideoAnalytics(currentdir + "/assets/Dining_Hall_Queue_Video_Generation.mp4",
                                        currentdir + "/assets/yolov8n.pt",
                                        "newrulesimportant.json",
                                        "https://mess-management-system-1f313-default-rtdb.firebaseio.com/")
                    print("Press \"D\" to Stop the Video")
                    count = va1.videoanalysis()
                    print(f"Video ended. Final count: {count}")
                case "2":
                    print("Coming Soon....")
                    time.sleep(2)
                case "3":
                    print("Coming Soon....")
                    time.sleep(2)
                case "4":
                    newuser.authenticated = False
    pass
if __name__ == "__main__":
    main()