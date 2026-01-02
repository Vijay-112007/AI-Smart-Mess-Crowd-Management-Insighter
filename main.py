from authentication import Authentication,SignIn,SignUp
import math
import numpy as np
import cv2 as cv

def main():
    # Create and sign up user
    newuser = SignUp("Vikram", "vikki1234", "vikram@gmail.com", 0)
    message = newuser.sign_up()
    print(message)
    
    # Sign in user
    signin = SignIn("Vikram", "vikki1234", 0)
    message2 = signin.sign_in()
    print(message2)
    
    # Create and sign up admin
    newadmin = SignUp("John", "john2999", "john@gmail.com", 1)
    message = newadmin.sign_up()
    print(message)
    
    # Sign in admin (create a SignIn instance, not call on SignUp)
    signin_admin = SignIn("John", "john2999", 1)
    message2 = signin_admin.sign_in()
    print(message2)
if __name__ == "__main__":
    main()