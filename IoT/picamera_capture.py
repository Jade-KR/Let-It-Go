import time
import picamera
import numpy as np
import cv2

from datetime import datetime

i = 1
with picamera.PiCamera() as camera:
  camera.resolution = (1280, 960)
  camera.framerate = 10
  while 1:
    image = np.empty((960, 1280, 3), dtype=np.uint8)
    camera.capture(image, 'bgr')
    print(i)
    i += 1
    cv2.imwrite("asdf-{}.bmp".format(datetime.now()), image)