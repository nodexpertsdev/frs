import cv2
import argparse
import time
import dlib
import imutils
import picamera
import io
import numpy
from imutils.video import VideoStream
from imutils import face_utils
from pymongo import MongoClient
from skimage import exposure


ap = argparse.ArgumentParser()
ap.add_argument("-r", "--picamera", type=int, default=-1,
	help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())

client=MongoClient('localhost', 27017)
db=client.empdata

vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
vs.vflip=True
VideoStream.resolution=(1000,1000)
VideoStream.vflip=True
vs.resolution=(1000,1000)
time.sleep(2.0)
detector=cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml')

Id=raw_input('enter your id')
empid=Id
empname=raw_input('Enter name: ')
empage=raw_input('Enter Age: ')
empco=raw_input('Enter employee country: ')
empem=raw_input('Enter email-id: ')

db.Employees.insert_one(
{
	"id":empid,
	"name":empname,
	"age":empage,
	"country":empco,
	"email":empem
	})
sampleNum=0
while(1):
    img = vs.read()
    img = imutils.resize(img, width=400,height=400)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray,1.1,5)
    cv2.imshow('frame',img)
    
    for (x,y,w,h) in faces:
        
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        
        #incrementing sample number 
        sampleNum=sampleNum+1
        #saving the captured face in the dataset folder
        cv2.imwrite("dataSet/User."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
        print sampleNum
        cv2.imshow('frame',img)
    #wait for 100 miliseconds
        
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break
    # break if the sample number is morethan 20
    elif sampleNum>9:
        break

vs.stop()
cv2.destroyAllWindows()

