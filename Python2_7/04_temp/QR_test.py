import argparse
import cv2
import datetime
import face_recognition
import imutils
import numpy as np
import pygame
import sqlite3 as sq
import time
import Tkinter as tk
import tkFont as tkfont
import tkMessageBox
import webbrowser

from ast import literal_eval
from imutils.video import VideoStream
from pygame import mixer
from pyzbar import pyzbar
from scipy.spatial import distance as dist


ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
                        help="path to output CSV file containing barcodes")
args = vars(ap.parse_args())

# initialize the video stream and allow the camera sensor to warm up
vs = VideoStream(src=0).start()
# vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

# open the output CSV file for writing and initialize the set of
# barcodes found thus far
csv = open(args["output"], "w")
found = set()

QR_status = True

while QR_status:
	# grab the frame from the threaded video stream and resize it to
	# have a maximum width of 400 pixels
	frame = vs.read()
	frame = imutils.resize(frame, width=400)

	# find the barcodes in the frame and decode each of the barcodes
	barcodes = pyzbar.decode(frame)

	if barcodes != []:
		for barcode in barcodes:
			# extract the bounding box location of the barcode and draw
			# the bounding box surrounding the barcode on the image
			(x, y, w, h) = barcode.rect
			cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 255), 2)

                    	# the barcode data is a bytes object so if we want to draw it
                    	# on our output image we need to convert it to a string first
                    	barcodeData = barcode.data.decode("utf-8")
                    	barcodeType = barcode.type
                    	print(barcodeData)
    
	# show the output frame
	cv2.imshow("Barcode Scanner", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
