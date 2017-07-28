import cv2,os
import numpy as np
from PIL import Image
from os import listdir
from os.path import isfile,join
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


recognizer = cv2.createLBPHFaceRecognizer()
detector= cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml')

def getImagesAndLabels(path):
    #get the path of all the files in the folder
    imagePaths=[f for f in listdir(path) if isfile(join(path, f))]
    
    #create empth face list
    faceSamples=[]
    #create empty ID list
    Ids=[]
    #now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        #loading the image and converting it to gray scale
        ip="/home/pi/FRSfinal/dataSet/"+imagePath
        pilImage=Image.open(ip).convert('L')
       
        #Now we are converting the PIL image into numpy array
        imageNp=np.array(pilImage,'uint8')
        #getting the Id from the image
        Id=int(os.path.split(imagePath)[-1].split(".")[1])
        
        # extract the face from the training image sample
        faces=detector.detectMultiScale(imageNp)
        
        #If a face is there then append that in the list as well as Id of it
        for (x,y,w,h) in faces:
            faceSamples.append(imageNp[y:y+h,x:x+w])
            Ids.append(Id)
    
    
    return faceSamples,Ids

faces,Ids = getImagesAndLabels("/home/pi/FRSfinal/dataSet")
recognizer.train(faces, np.array(Ids))
print "Faces trained"
recognizer.save('trainner/trainner.yml')


