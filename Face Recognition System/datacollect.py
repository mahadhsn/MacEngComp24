import cv2
import os
from PIL import Image
import numpy as np


video=cv2.VideoCapture(0)

facedetect=cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

count=0

nameID=str(input("Enter Your Name: ")).lower()
num_of_images=100

path='images/'+nameID

isExist = os.path.exists(path)

if isExist:
	print("Name Already Taken")
	nameID=str(input("Enter Your Name Again: "))
else:
	os.makedirs(path)

while True:
	ret,frame=video.read()
	faces=facedetect.detectMultiScale(frame,1.3, 5)
	for x,y,w,h in faces:
		image = frame[y:y+h,x:x+w]
		gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		final_image = cv2.resize(gray_image, (300,300))
		count=count+1
		name='images/'+nameID+'/'+str(count)+ '.jpg'
		print("Creating Images........." +name)
		cv2.imwrite(name, final_image)
		cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 3)

	cv2.imshow("WindowFrame", frame)
	cv2.waitKey(1)
	
	if count>num_of_images:
		break
video.release()
cv2.destroyAllWindows()