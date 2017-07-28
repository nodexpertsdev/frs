#echo "sendgrid.env" >> .gitignore
#source ./sendgrid.env

import cv2
import numpy as np
import argparse
import time
import dlib
import imutils
import picamera
import io
from imutils.video import VideoStream
from imutils import face_utils
from pymongo import MongoClient
import sendgrid
import os
from sendgrid.helpers.mail import *
import httplib, urllib, base64
import pyimgur

def uploadimg(s):
	CLIENT_ID = "abfb53f45140aa6"
	PATH = s
	
	im = pyimgur.Imgur(CLIENT_ID)
	uploaded_image = im.upload_image(PATH, title="Uploaded with PyImgur")
	print(uploaded_image.title)
	s=(uploaded_image.link)
	print s
	emotion(s)
	print(uploaded_image.size)
	print(uploaded_image.type)

def emotion(s):
	s=s+"'}"
	body = "{ 'url':'"
	body=body+s

	try:
	    # NOTE: You must use the same region in your REST call as you used to obtain your subscription keys.
	    #   For example, if you obtained your subscription keys from westcentralus, replace "westus" in the 
	    #   URL below with "westcentralus".
	    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
	    conn.request("POST", "/emotion/v1.0/recognize?%s" % params, body, headers)
	    response = conn.getresponse()
	    
	    data = response.read().split(",")
	    
	    tmp=[]
	    maxstr=[]
	    tmp=data[4].split("{")
	    maxstr=tmp[1].split(":")
	    #print float(maxstr[1])
	    for i in range(5,11):
	        tmp=[]
	        tmp=data[i].split(":")
	        if float(tmp[1])>float(maxstr[1]):
	            #print "change"
	            maxstr[1]=tmp[1]
	            maxstr[0]=tmp[0]
	        #print data[i]
	
	     
	    tmp=[]
	    tmp=data[11].split("}")
	    tmp1=[]
	    tmp1=tmp[0].split(":")
	    if float(tmp1[1])>float(maxstr[1]):
	             maxstr[1]=tmp1[1]
	             maxstr[0]=tmp1[0]
	    print maxstr
	    
	    conn.close()
	except Exception as e:
	    print("[Errno {0}] {1}".format(e.errno, e.strerror))



headers = {
    # Request headers. Replace the placeholder key below with your subscription key.
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'b4137f50b56e4e8e9b1a51465ca4365e',
}

params = urllib.urlencode({
})


client=MongoClient('localhost',27017)
db=client.empdata
ap = argparse.ArgumentParser()

sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
from_email = Email("test@example.com")

ap.add_argument("-r", "--picamera", type=int, default=-1,
	help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())

recognizer = cv2.createLBPHFaceRecognizer()
recognizer.load('trainner/trainner.yml')
cascadePath = '/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml'
faceCascade = cv2.CascadeClassifier(cascadePath);


vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
vs.vflip=True
VideoStream.resolution=(100,100)

vs.resolution=(100,100)
time.sleep(2.0)
k=0
a=[]
previous=0
for i in range(20):
    a.append(0)
dobreak=0
while True:
    im =vs.read()
    gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    faces=faceCascade.detectMultiScale(gray, 1.2,5)
    for(x,y,w,h) in faces:
        
        Id, conf = recognizer.predict(gray[y:y+h,x:x+w])
	
        if(conf>49):
            cv2.rectangle(im,(x,y),(x+w,y+h),(0,0,255),3)
            
        else:
            #read(Id)
	    a[Id]=a[Id]+1
	    print Id
	    if previous!=Id:
		a[previous]=0
	    for i in range(0,20):
		if a[i]==5:
			empcol=db.Employees.find({"id":str(i)},{"name": 1,"email":1})
			for emp in empcol:
				print ("Hello %s !!!" %emp["name"])
				cv2.imwrite("tmp.jpg",im)
				s="/home/pi/FRSfinal/tmp.jpg"
				#uploadimg(s)
				to_email = Email(emp["email"])
				subject = "Face Recognised"
				content = Content("text/plain", "Hello %s" %emp["name"])
				mail = Mail(from_email, subject, to_email, content)
				k=1
				print "Mail Sent"
				response = sg.client.mail.send.post(request_body=mail.get())
				print(response.status_code)
				print(response.body)
				print(response.headers)
			dobreak=1
			break
		previous=Id
		#print "Please wait..."
		
            cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),3)
        
    cv2.imshow('im',im) 
    if dobreak==1:
	break
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
vs.stop()
cv2.destroyAllWindows()
