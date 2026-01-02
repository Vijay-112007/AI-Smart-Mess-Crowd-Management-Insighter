import cv2
import numpy as np
import csv
import os
import datetime
import random
#in order to access the app we need maintain the authentication
#two options are avaible one is sign in and sign up 
from abc import ABC
class Authentication(ABC):
    def sign_in(self):
        pass
    def sign_up(self):
        pass
    def options(self):
        print(f"1. Login In \n 2. Sign Up")
#the authentication class is abstract class whihc helps to prevent the options from the data insecurity it hides the data implementation
#now for the sake of time we will store all the login credentials in a file after we will shift it to the firebase database
#in this class we need to catch the return messages
class SignIn(Authentication):
    def __init__(self,user_name,passcode,admin = 1):
        self.user_name = user_name
        self.passcode = passcode
        self.authenticated = False
        self.isadmin = admin
    def sign_up(self):
        email = input("Enter Your Email:")
        sign_up_instance = SignUp(self.user_name, self.passcode, email, self.isadmin)
        signup_result = sign_up_instance.sign_up()
        if "Successfully Created" in signup_result:
            # After successful signup, sign in
            return sign_up_instance.sign_in()
        else:
            return signup_result
    def sign_in(self):
        #after retreving the login credentials we should check either there exists a user name or not if exists we will 
        #check for the passcode authentication
        #we had created a file in order to store the credentials called as credentials.csv
        #first open the file
        currentdir = os.getcwd()
        if self.isadmin == 0:
            path = os.path.join(currentdir,"credentials.csv")
            with open(path,"r") as fd:
                csvreader = csv.reader(fd)
                header = next(csvreader)
            #now we will check either the name is correct or not
                for row in csvreader:
                    if len(row) > 1 and row[1] == self.user_name:
                        # Assuming second column is username, third is password
                        if len(row) > 2 and row[2] == self.passcode:
                            self.authenticated = True
                            return "Authentication Successfull"
                        else:
                            return "Incorrect Credentials"  # Username found but password wrong
                return "Incorrect Credentials" #user name is not correct
        elif self.isadmin == 1:
            path = os.path.join(currentdir,"admincred.csv")
            with open(path,"r") as fd:
                csvreader = csv.reader(fd)
                header = next(csvreader)
            #now we will check either the name is correct or not
                for row in csvreader:
                    if len(row) > 1 and row[1] == self.user_name:
                        # Assuming second column is username, third is password
                        if len(row) > 2 and row[2] == self.passcode:
                            self.authenticated = True
                            return "Authentication Successfull for Admin"
                        else:
                            return "Invalid Admin Credentials"  # Username found but password wrong
                return "Invalid Admin Credentials" #user name is not correct
#After the authentication we need to catch the messages and the other options are only allowed if the self.authenticated = True
#now we will do the sign up option which leads to new user creation and helps us to make the things correctly
class SignUp(Authentication):
    def __init__(self,new_user_name,new_passcode,email,admin = 1):
        self.username = new_user_name
        self.passcode = new_passcode
        #logic should be like after intialization ti should be like directly go into the sign_up section without pressing any thing from the user
        self.email = email
        self.isadmin = admin
    def sign_in(self):
        # Use the SignIn class method with the same username and passcode
        signin_instance = SignIn(self.username, self.passcode, self.isadmin)
        sign_in_result = signin_instance.sign_in()
        return sign_in_result
    def recovery_code(self):
        #first we will find the recorvery code then we will create the account
        #we will create a seed using the user_name + email then use it as seed then generate random number then use that 
        #random number as recovery code
        seed = self.username + self.email
        random.seed(seed)
        self.number = random.randint(10000,99999)
        return self.number
    #this is the recovery codes of the account which is useful for the account forget option
    def sign_up(self):
        #if we need to sign up into the account we need to get
        #the essential details in order to create the account
        #first we need to check either the email is already registered or not
        #so load the file and check for the details
        currentdir = os.getcwd()
        if self.isadmin == 0:
            path = os.path.join(currentdir,"credentials.csv") 
            with open(path,"r") as fd:
                csvreader = csv.reader(fd)
                header = next(csvreader)
                for row in csvreader:
                        if row[3].strip() == self.email:
                            return "Email already Registered"
                #now if the email isn't registered we need to create means add the details inside the csv file
                code = self.recovery_code()
            with open(path,"a",newline= "") as fd:
                time = str(datetime.datetime.now())
                csvwriter = csv.writer(fd)
                fd.write('\n')
                csvwriter.writerow([time, self.username, self.passcode, self.email,code])
            return "Account Successfully Created"
        elif self.isadmin == 1:
            path = os.path.join(currentdir,"admincred.csv")
            with open(path,"r") as fd:
                csvreader = csv.reader(fd)
                header = next(csvreader)
                for row in csvreader:
                        if row[3].strip() == self.email:
                            return "Admin already Registered"
                #now if the email isn't registered we need to create means add the details inside the csv file
                code = self.recovery_code()
            with open(path,"a",newline= "") as fd:
                time = str(datetime.datetime.now())
                csvwriter = csv.writer(fd)
                fd.write('\n')
                csvwriter.writerow([time, self.username, self.passcode, self.email,code])
            return "Account Successfully Created For New Admin"