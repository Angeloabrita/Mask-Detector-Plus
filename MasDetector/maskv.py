from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import tensorflow 
import numpy as np
import time
import cv2
import os
import playsound
import dataControler

import locale
loc = locale.getdefaultlocale()

def os_path():
    ''' This create dir inside user documente
     and retorn string path'''

    home = os.path.expanduser('~')
    folder_path = os.path.join(home,'Documents\mask-infraction')
    check = os.path.isdir(folder_path)

    if not check:
        try:
            os.mkdir(folder_path)
        except OSError:
            return ("Creation of the directory %s failed" % folder_path)
        else:
           return folder_path
    else:
        return folder_path

def detect_and_predict_mask(frame, faceNet, maskNet):
	# grab the dimensions of the frame and then construct a blob
	# from it
	(h, w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),
		(104.0, 177.0, 123.0))

	# pass the blob through the network and obtain the face detections
	faceNet.setInput(blob)
	detections = faceNet.forward()

	# initialize our list of faces, their corresponding locations,
	# and the list of predictions from our face mask network
	faces = []
	locs = []
	preds = []

	# loop over the detections
	for i in range(0, detections.shape[2]):
		# extract the confidence (i.e., probability) associated with
		# the detection
		confidence = detections[0, 0, i, 2]

		# filter out weak detections by ensuring the confidence is
		# greater than the minimum confidence
		if confidence > 0.5:
			# compute the (x, y)-coordinates of the bounding box for
			# the object
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")

			# ensure the bounding boxes fall within the dimensions of
			# the frame
			(startX, startY) = (max(0, startX), max(0, startY))
			(endX, endY) = (min(w - 1, endX), min(h - 1, endY))

			# extract the face ROI, convert it from BGR to RGB channel
			# ordering, resize it to 224x224, and preprocess it
			face = frame[startY:endY, startX:endX]
			face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
			face = cv2.resize(face, (224, 224))
			face = img_to_array(face)
			face = preprocess_input(face)

			# add the face and bounding boxes to their respective
			# lists
			faces.append(face)
			locs.append((startX, startY, endX, endY))

	# only make a predictions if at least one face was detected
	if len(faces) > 0:
		# for faster inference we'll make batch predictions on *all*
		# faces at the same time rather than one-by-one predictions
		# in the above `for` loop
		faces = np.array(faces, dtype="float32")
		preds = maskNet.predict(faces, batch_size=32)

	# return a 2-tuple of the face locations and their corresponding
	# locations
	return (locs, preds)


# load our serialized face detector model from disk
print("[INFO] loading face detector model...")
prototxtPath = os.path.sep.join(["face_detector", "deploy.prototxt"])
weightsPath = os.path.sep.join(["face_detector",
	"res10_300x300_ssd_iter_140000.caffemodel"])

# prototxtPath = "face_detector/deploy.prototxt"
# weightsPath = "face_detector/res10_300x300_ssd_iter_140000.caffemodel"

faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

# load the face mask detector model from disk
print("[INFO] loading face mask detector model...")
maskNet = load_model("mask_detector.model")

# # initialize the video stream and allow the camera sensor to warm up
# print("[INFO] starting video stream...")
video = cv2.VideoCapture(0) #VideoStream(src=0).start()


time.sleep(2.0)

#--set global values to  people with mask now and total
whithMaskFrame = 0
noMaskFrame = 0

totalWithMask = 0
totalNoMask = 0

nowTotal = 0 

nowlWithMask = 0
nowlNoMask = 0

def streaming(frame1):
	
	frame = frame1	
	# detect faces in the frame and determine if they are wearing a
	# face mask or not
	(locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)

	# get total, with and without detected 
	global nowlWithMask,nowlNoMask , nowTotal
	
	nowTotal = len(preds)
	nowlWithMask = len([i for i in preds if i[0]>i[1]])
	nowlNoMask = len([i for i in preds if i[0]<i[1]])

	# loop over the detected face locations and their corresponding
	for (box, pred) in zip(locs, preds):
		# unpack the bounding box and predictions
		(startX, startY, endX, endY) = box
		(mask, withoutMask) = pred
	
		# determine the class label and color we'll use to draw
		# the bounding box and text
		if mask > withoutMask:
				
			label = "Com mascara" 
			#set data after x frames
			global whithMaskFrame, totalWithMask		
			whithMaskFrame +=1
			
			if whithMaskFrame > 10 and whithMaskFrame <12:
				totalWithMask +=1
				dataControler.pushData("WithMask")
					
		else:

			label ="Sem Mascara"
			#set data after x frames		
			global noMaskFrame, totalNoMask
			noMaskFrame +=1

			if noMaskFrame > 10 and noMaskFrame <12:
				totalNoMask +=1
				dataControler.pushData("NoMask")

				#take a pic and save in documents/infractions
				timestr = time.strftime("%d-%m-%Y_%H-%M-%S")
				cv2.putText(frame, timestr, (startX, startY - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.50, (0, 0, 255), 2)				
				cv2.imwrite(os_path() +'\img_' + timestr + '.jpg',frame)

			#start song alarm after x frame
			if noMaskFrame > 60:
				if loc[0]=="pt_BR": playsound.playsound("songs/ptbr.mp3") 
				else: playsound.playsound("songs/en.mp3")
				

		#set to 0 framerate 
		if label == "Com mascara":
			color = (0, 255, 0)
			noMaskFrame = 0
			
		else:
			whithMaskFrame = 0
			color = (0, 0, 255)

		#draw retangle with label
		cv2.putText(frame, label, (startX, startY - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
		cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
	
	return frame



