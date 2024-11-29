import numpy as np
import cv2
import numpy as np
import random
import os
import face_recognition

facedetect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

cap=cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
font=cv2.FONT_HERSHEY_COMPLEX

mahad_image = face_recognition.load_image_file('images/mahad/1.jpg')
mahad_face_encoding = face_recognition.face_encodings(mahad_image)[0]

harsh_image = face_recognition.load_image_file('images/harsh/92.jpg')
harsh_face_encoding = face_recognition.face_encodings(harsh_image)[0]

dharav_image = face_recognition.load_image_file('images/dharav/99.jpg')
dharav_face_encoding = face_recognition.face_encodings(dharav_image)[0]

known_face_encodings = [
    mahad_face_encoding,
	harsh_face_encoding,
	dharav_face_encoding
]
known_face_names = [
    "Mahad",
	"Harsh",
	"Dharav"
]

original_img2 = cv2.imread('images/mahad/1.jpg')
img2_encoding = face_recognition.face_encodings(original_img2)[0]
image_count = 101


face_locations = []
face_encodings = []
face_name = []
s = True
matches = False
name = ""
num_of_faces=0
last_num_of_faces=0

while True:
	sucess, imgOrignal=cap.read()
	small_frame = cv2.resize(imgOrignal, (0, 0), fx=0.25, fy=0.25)
	rgb_small_frame = small_frame[:, :, :]
	faces = facedetect.detectMultiScale(imgOrignal,1.3,5)
	
	for face in faces:
		different_faces = dict()
		num_of_faces = len(faces)
		face_locations = face_recognition.face_locations(rgb_small_frame)
		face_encodings = face_recognition.face_encodings(rgb_small_frame,face_locations)	
		face_names = []
		for face_encoding in face_encodings:
			matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
			name = ""
			face_distance = face_recognition.face_distance(known_face_encodings, face_encoding)
			best_match_index = np.argmin(face_distance)
			if matches[best_match_index]:
				name = known_face_names[best_match_index]
			face_names.append(name)

		different_faces[str(face)] = name
		last_num_of_faces = num_of_faces

	for face in faces:
		num_of_faces = len(faces)
		if num_of_faces != last_num_of_faces:
			continue
		x,y,w,h=face
		if str(face) in different_faces:
			name = different_faces[str(face)]
		else:
			name = ""
   
		if name != "":
			cv2.rectangle(imgOrignal,(x,y),(x+w,y+h),(0,255,0),2)
			cv2.rectangle(imgOrignal, (x,y-40),(x+w, y), (0,255,0),-2)
			cv2.putText(imgOrignal, str(name),(x,y-10), font, 0.75, (255,255,255),1, cv2.LINE_AA)
		else:
			cv2.rectangle(imgOrignal,(x,y),(x+w,y+h),(0,0,255),2)
			cv2.rectangle(imgOrignal, (x,y-40),(x+w, y), (0,0,255),-2)
			cv2.putText(imgOrignal, "Unknown",(x,y-10), font, 0.75, (255,255,255),1, cv2.LINE_AA)
		name = ""

  
	cv2.imshow("Result",imgOrignal)
	k=cv2.waitKey(1)
	if k==ord('q') & 0xFF == ord('q'):
		break


cap.release()
cv2.destroyAllWindows()