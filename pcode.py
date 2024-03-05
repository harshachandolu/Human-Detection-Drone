import numpy as np
import time
import cv2
import os
import time

import urllib.request
import requests
def nothing(x):
    pass

 
#change the IP address below according to the
#IP shown in the Serial monitor of Arduino code
url='http://192.168.93.192/cam-lo.jpg'
url1='http://192.168.93.192/'
 
time.sleep(2)
print('Started..')
harcascadePath = "haarcascade_frontalface_default.xml"
detector=cv2.CascadeClassifier(harcascadePath)
sampleNum=0
while True:
       

                img_resp=urllib.request.urlopen(url)
                imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
                frame=cv2.imdecode(imgnp,-1)
                #(grabbed, frame) = vs.read()
                
                response = requests.get(url1)

                print(response.content)
                try:
                    pval=(str(response.content).split(':')[1].split('}')[0])
                except:
                    pval=0
                print('PIR:'+str(pval))
                if(pval==str(1)):
                    cv2.imwrite('PIR_'+str(sampleNum) + ".jpg", frame)
                    cv2.waitKey(1)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x,y,w,h) in faces:
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)        
                    #incrementing sample number 
                    sampleNum=sampleNum+1
                    #saving the captured face in the dataset folder TrainingImage
                    cv2.imwrite(str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                    #display the frame
                cv2.imshow('frame',frame)
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
