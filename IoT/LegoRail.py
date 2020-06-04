import requests
import json
from getpass import getpass
import hashlib
import serial
import cv2
from picamera import PiCamera
from time import sleep
from datetime import datetime
import numpy as np
'''
baseURL = "http://192.168.0.220:8766/api/"
sha256 = hashlib.sha256()
sha256.update("asdf".encode('utf-8'))
data = dict()
data["username"] = input("ID:")
data["password"] = getpass("PASSWORD:")
while 1:
  a = requests.post(baseURL + "login/", json=data)
  if a.status_code == 200:
    headers = {
      "Authorization": "jwt " + a.json()["token"]
    }
    break
  else:
    print("id or password error")
    data["username"] = input("ID:")
    data["password"] = getpass("PASSWORD:")
print("login success")

'''
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
bg_img = cv2.imread("bg_img.bmp")
print(bg_img.shape)
bg_b, bg_g, bg_r = cv2.split(bg_img)
print(bg_g.shape, bg_b.shape, bg_r.shape)

cap_idx = 0
with PiCamera() as camera:
  camera.resolution = (1280, 960)
  camera.framerate = 10
  image = np.empty((960, 1280, 3), dtype=np.uint8)
  while 1:
    if ser.in_waiting:
      print(ser.read(3))
      camera.capture(image, 'bgr')
      #cv2.imwrite("original_{}.bmp".format(cap_idx), image)
      #cap_idx += 1
      img_b, img_g, img_r = cv2.split(image)
      
      diff_b = cv2.absdiff(bg_b, img_b)
      diff_g = cv2.absdiff(bg_g, img_g)
      diff_r = cv2.absdiff(bg_r, img_r)
      
      ret_b, img_tresh_b = cv2.threshold(diff_b, 100, 255, cv2.THRESH_BINARY)
      ret_g, img_tresh_g = cv2.threshold(diff_g, 100, 255, cv2.THRESH_BINARY)
      ret_r, img_tresh_r = cv2.threshold(diff_r, 100, 255, cv2.THRESH_BINARY)
      
      img_tresh_all = img_tresh_b + img_tresh_g + img_tresh_r
      
      diff_gray_blur = cv2.GaussianBlur(img_tresh_all, (5, 5), 0)
      
      ret, img_tresh = cv2.threshold(diff_gray_blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
      
      a2, arr_cnt, _ = cv2.findContours(img_tresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
      #print(arr_cnt)
      #print(a2)
      #print(_)
      #img_with_allcontours = image.copy()
      
      #cv2.drawContours(img_with_allcontours, arr_cnt, -1, (0, 255, 0), 3)
      
      height, width, channels = image.shape
      
      w = width
      h = height
      
      validcontours = []
      contour_index = -1
      
      for i in arr_cnt:
        contour_index += 1
        ca = cv2.contourArea(i)
        
        x, y, w, h = cv2.boundingRect(i)
        
        aspect_ratio = float(w)/h
        
        edge_noise = False
        if x == 0 or y == 0:
          edge_noise = True
          
        if x+w ==width or y+h == height:
          edge_noise = True
        if ca > 1300:
          if aspect_ratio <= 6:
            if edge_noise == False:
              validcontours.append(contour_index)
      #img_withcontours = image.copy()
      
      #for k in range(len(validcontours)):
      #  cv2.drawContours(img_withcontours, arr_cnt, validcontours[k], (0, 255, 0), 3)
      
      
      add = 40
      limit = 70
      object_position = []
      for j in validcontours:
        x, y, w, h = cv2.boundingRect(arr_cnt[j])
        c_x = x + int(w//2)
        c_y = y + int(h//2)
        n_w = int(w//2) + add
        n_h = int(h//2) + add
        if c_x + n_w < width - limit and c_y + n_h < height - limit and 0 + limit <= c_x - n_w and 0 + limit <= c_y - n_h:
          if w > h:
            object_position.append((c_x-n_w, c_y-n_w, c_x+n_w, c_y+n_w))
          else:
            object_position.append((c_x-n_h, c_y-n_h, c_x+n_h, c_y+n_h))
      k = 1
      
      selected_lego = []
      max_length = 0
      for p in object_position:
        try:
          if p[3] - p[1] > max_length:
            selected_lego = p
        except:
          continue
      if selected_lego:
        img = image[selected_lego[1]:selected_lego[3], selected_lego[0]:selected_lego[2]]
        cv2.imwrite("cropped_img_{}.bmp".format(datetime.now()), img)
        
        
        '''
        previewImg('selected_lego',img_example[selected_lego[1]:selected_lego[3], selected_lego[0]:selected_lego[2]])
      print(object_position)
      
      for p in object_position:
        try:
          img = image[p[1]:p[3], p[0]:p[2]]
          cv2.imwrite("cropped_img_{}.bmp".format(datetime.now()), img)
          k += 1
        except:
          continue
          '''
      
      #if ser.read().encode('ascii')=='1':
"""      res = ser.read()
    if res==1:
      # image processing
      
      # write serial
      c = "3".encode('utf-8')
    ser.write(b'\x4c\xff\x46')
    """  


try:
  while(cap.isOpened()):
    ret, frame = cap.read()
    cv2.im
    if(ret):
      cv2.imshow('res', frame)
      sleep(10)
      gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      cv2.imshow('res', gray_img)
      print(ret)
      frame = cv2.flip(frame, 0)
      cv2.imshow("res", frame)
  cap.release()
  cv2.imshow('img', frame)
  input("OK")
  #ser.open()
  #ser.write("write".encode("ascii"))
  try:
    while 1:
      ser.write(input("input").encode())
      response = ser.readline()
      while not response:
        response = ser.readline()
      print(response.decode("utf-8"))
  except KeyboardInterrupt:
    ser.close()
  #sha256 = hashlib.sha256()
  #sha256.update("asdf".encode('utf-8'))
  #print(sha256.hexdigest())
  data = dict()
  data["username"] = input("ID:")
  data["password"] = getpass("PASSWORD:")
  while 1:
    a = requests.post('http://192.168.0.220:8766/api/login/', json=data)
    if a.status_code == 200:
      headers = {
        "Authorization": "jwt " + a.json()["token"]
      }
      break
    else:
      print("id or password error")
      data["username"] = input("ID:")
      data["password"] = getpass("PASSWORD:")
  print("login success")
  
  
  part_list = [
    {
      "part_id": "004229",
      "color_id": 0
    },
    
    {
      "part_id": "004229",
      "color_id": 1
    },
    {
      "part_id": "004229",
      "color_id": 0
    },
    {
      "part_id": "004229",
      "color_id": 2
    }
  ]
  
  for part in part_list:
    requests.post('http://192.168.0.220:8766/api/UpdateUserPart2', json=part, headers=headers)

except KeyboardInterrupt:
  cap.release()