# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import getpass
import cv2
import os
import cv2
import numpy as np
from csv import writer
from datetime import datetime
import pandas as pd


# datetime object containing current date and time
def get_time():

    now = datetime.now()
    # dd/mm/YY H:M:S
    curr_date = now.strftime("%d/%m/%Y")
    curr_time=now.strftime(" %H:%M:%S")
    print(curr_time+" "+curr_date)
    return  curr_time
def get_date():

    now = datetime.now()
    # dd/mm/YY H:M:S
    curr_date = now.strftime("%d/%m/%Y")
    curr_time=now.strftime(" %H:%M:%S")
    print(curr_time+" "+curr_date)
    return  curr_date

class user(object):
    ID=0
    def __init__(self,first,last,username,password,pic):
        self.first=first
        self.last=last
        self.username=username
        self.password=password
        self.email=username+"@org.com"
        user.ID +=1
        self.ID=user.ID
        self.pic=pic
    def disp_data(self):
        data=self.first+"\t"+ self.last +"\t"+ self.username+"\t"+self.attendance_day+"\t"+self.attendance_day+"\n"
        print(data)
    def get_my_attendance(self,x,y):
        self.attendance_time=x
        self.attendance_day=y
        print("user attendance saved"+ x +"  "+y)

def data_to_list():
    user_list = []

    df = pd.read_csv("user_data.csv")
    for row in range (0,len(df.index)):
        user_list=list(df.loc[row])
        temp_user = user(user_list[0], user_list[1], user_list[2], user_list[4], user_list[5])
        temp_user.ID=user_list[3]
        temp_user.attendance_time = user_list[7]
        temp_user.attendance_day= user_list[8]
        users.append(temp_user)
        user_list.clear()
    for a in users:
        print(a.username)

def append_list_as_row(file_name):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        user_data=[]
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        for user in users:
            user_data.append(user.first)
            user_data.append(user.last)
            user_data.append(user.username)
            user_data.append(user.ID)
            user_data.append(user.password)
            user_data.append(user.pic)
            user_data.append(user.email)
            user_data.append(user.attendance_time)
            user_data.append(user.attendance_day)
            csv_writer.writerow(user_data)
            user_data.clear()


import face_recognition
users=[]
def face_rec(user):
        path='E:\C++'
        imgs=[]
        curimg = cv2.imread(user.pic)
        curimg=cv2.cvtColor(curimg,cv2.COLOR_BGR2RGB)
        user_encode=face_recognition.face_encodings(curimg)[0]
        print("encoding done for "+ user.pic)
        cap=cv2.VideoCapture(0)

        while True:
            success,img=cap.read()
            imgS=cv2.resize(img,(0,0),None,0.25,0.25)
            imgS=cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)

            facesCurFrame=face_recognition.face_locations(imgS)[0]
            encodesCurFrame=face_recognition.face_encodings(imgS)[0]
            matches=face_recognition.compare_faces([user_encode],encodesCurFrame)
            #faceDis=face_recognition.face_distance(user_encode,encodeFace)
            print(matches)
            if matches[0] == True:
                x=get_time()
                y=get_date()
                user.get_my_attendance(x,y)
                break
            cv2.imshow("webcam", img)
            cv2.waitKey(1)




def get_object(username ,password):

    for obj in users:
        if str(obj.password) == str(password) and str(obj.username) == str(username):
            return obj
    return 0
def delete_user(user):
    id=user.ID
    username=user.username
    count=0
    for obj in users:
        if obj.ID == id and obj.username == username :
            users.pop(count)
            delete_file(id,username)
        count += 1
def delete_file(id,user):

    if os.path.exists(str(id)+"_"+user+".png"):
        os.remove(str(id)+"_"+user+".png")
    else:
        print("The file does not exist")



def startup_page():
    a=input('hello press U for sign up and I for sign in ')
    if a=='U' or a=='u':
        signup_page()
    elif a=='I' or a=='i':
        login_page()
    else:
        return
def login_page():
    while (1):
        key=0
        username=input("enter username: \n")
        password=input("enter password: \n")
        curr_user=get_object(username,password)
        if curr_user == 0:
            key=1
            print("user input error try again  \n")
        if key == 0:
            break
    user_page(curr_user)
def user_page(user):
    print("welcome "+ user.first )
    delete = input("press D if you want to delete user or A if you want the attendance")
    if delete == 'd':
        delete_user(user)
    elif delete == 'a':
        face_rec(user)
    startup_page()

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
def signup_page():
    first=input(" enter first name:\t")
    last = input(" enter last name:\t")
    while(1):
        key=0
        username = input(" enter username:\t")

        for obj in users:
            if obj.username == username:
                key=1
                print("invalid username already exists \n")
        if key==0:
            break

    password =input(" enter password:\t")

    new_user=user(first,last,username,password,"aaa")
    users.append(new_user)
    print("please press space when your face is positioned well")
    get_my_pic(new_user)
    delete =input("press D if you want to delete user or A if you want the attendance or O to log out")
    if delete =='d':
        delete_user(new_user)
    elif delete == 'a':
        face_rec(new_user)
    startup_page()

def get_my_pic(user):
    cam = cv2.VideoCapture(0)

    cv2.namedWindow("Press space to get your pic")

    img_counter = 0

    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test", frame)

        k = cv2.waitKey(1)
        if k % 256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k % 256 == 32:
            # SPACE pressed
            img_name =user.username+".png".format(img_counter)
            user.pic=user.username+".png"
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1

            break

    cam.release()

    cv2.destroyAllWindows()
data_to_list()
startup_page()
append_list_as_row('user_data.csv')
