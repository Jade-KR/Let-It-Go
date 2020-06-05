import requests
import json
from getpass import getpass
import hashlib
import serial
import cv2
from picamera import PiCamera
from time import sleep
from datetime import datetime

datetime.now()



cap = cv2.VideoCapture(-1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
a = 1

while(True):
  ret, frame = cap.read()
  cv2.imwrite("asdf-{}.jpg".format(datetime.now()), frame)
  print(a)
  a += 1
  sleep(1)