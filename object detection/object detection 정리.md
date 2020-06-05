# Object Detection

## Object Detection이란?

- 이미지나 동영상에서 사람, 동물, 차량 등 의미 있는 객체(object)의 종류와 그 위치(bounding box)를 정확하게 찾기 위한 컴퓨터 비전 기술.

- 영상에서 관심 대상을 인식하기 위해 일반적으로 검출 대상에 대한 후보 영역을 찾고 그 후보 영역에 대한 객체의 종류와 위치를 학습된 모델을 통해 예측한다. 이 과정을 위해서 영상 및 영상 내의 객체 종류(class)와 객체 위치(bounding box) 정보가 필요하다. 얼굴, 도로상의 보행자 및 차량 등의 인식에 딥 러닝(deep learning) 기반의 객체 탐지 기술이 많이 이용된다.

출처: 네이버 지식백과, 객체 탐지[object detection, 客體探知] (IT용어사전, 한국정보통신기술협회)



## Object Detection의 순서도

- 영상이나 이미지가 들어오면 한 부분에 물체가 있다는걸 인식 (Object Recognition)하고, 그 물체가 무엇인지 분류(Object Classification)하고 정확한 위치를 찍어줌(Object Localization). 

- Object Classification와 Object Localization를 합쳐서 Object Detection이라고 부름.

![OD_flow_chart](images/OD_flow_chart.PNG)



- Object Recognition과 Object Detection에 대하여 그 의미가 혼용되거나 다르게 사용되는 경우도 존재함

- 대부분은 Object Classification와 Object Localization를 합쳐서 Object Detection이라고 부름



## Object Detection의 역사

- 2012년 이전, '영상처리'로만 해결했었음

- 그 이후, 컴퓨팅파워가 발전하고 인터넷에 많은 데이터가 쌓이면서 딥러닝이 활용되기 시작함

- Two-shot-detection(초기 버전)

  - 영상이나 이미지 전체를 Sliding하면서 계속 네트워크를 돌려줌
  - 한장의 이미지에 엄청나게 많은 연산량이 필요함
  - 실시간성 zero

- Two-shot-detection (업그레이드 버전)

  ![Two-shot-detection](images/Two-shot-detection.PNG)

  - 이미지 전체에 대해서가 아니라 물체가 있을 것이라고 생각되는 부분들만 box 형태로 잘라냄
  - 그 결과들에 대해서 CNN 사용
  - ex) R-CNN, F-CNN, R-FCN, FPN-FRCN, Fast R-CNN

- One-shot-detection

  ![Two-shot-detection](images/One-shot-detection.PNG)

  - 하나의 신경망을 통과하여 물체의 bounding box와 class를 동시에 예측하게 됨
  - ex) YOLO, SSD, RetinaNet



## One-shot-detection vs Two-shot-detection?

- One-shot-detection
  - 장점: 높은 실시간성
  - 단점: Two-shot-detection보다 상대적으로 정확도가 떨어짐
- Two-shot-detection
  - 장점: 높은 정확도
  - 단점: 느린 속도
- 현재는 두개의 알고리즘 모두 계속 개발 되어 가고 있음



출처: https://mickael-k.tistory.com/24



## 'LET IT GO'에서의 Object Detection

- 1단계: 컨베이어 벨트에 올려진 레고들의 위치를 인식하고 적절한 크기로 잘라내는 과정 
  - 'Object Detection의 순서도'에서 Object Recognition과 Object Localization를 동시에 처리한다고 볼 수있음
- 2단계: 그 결과를 통해 학습된 CNN 모델로 레고를 분류(Object Classification)

- Two-shot-detection을 사용한다고 할 수 있음



## 1단계: Object Recognition + Object Localization

























```python
import cv2
import numpy as np
import os
from matplotlib import pyplot as plt

def previewImg(text,img_preview,grayscale=False):
    # plt.imshow(img_preview)
    if grayscale==False:
        #convert a color image from BGR to RGB before previewing
        plt.imshow(cv2.cvtColor(img_preview, cv2.COLOR_BGR2RGB))
    else:
        #option for Grayscale images
        plt.imshow(cv2.cvtColor(img_preview, cv2.COLOR_GRAY2RGB))
    plt.title(text)
    plt.show()
    
lego_images = os.listdir('gdrive/My Drive/Colab Notebooks/input/various')
# lego_images = os.listdir('gdrive/My Drive/Colab Notebooks/input/various_bg')
img_bg=cv2.imread('gdrive/My Drive/Colab Notebooks/input/various_bg.jpg')

for index in range(len(lego_images)):
  img_example=cv2.imread('gdrive/My Drive/Colab Notebooks/input/various/{}'.format(lego_images[index]))

  example_b, example_g, example_r = cv2.split(img_example)
  back_b, back_g, back_r = cv2.split(img_bg)

  diff_b=cv2.absdiff(back_b,example_b)
  diff_g=cv2.absdiff(back_g,example_g)
  diff_r=cv2.absdiff(back_r,example_r)

  # img_bg_gray=cv2.cvtColor(inversebgr, cv2.COLOR_BGR2GRAY)
  # ret_b, img_tresh_b = cv2.threshold(diff_b, 100, 255,cv2.THRESH_BINARY)
  ret_b, img_tresh_b = cv2.threshold(diff_b, 100, 255,cv2.THRESH_BINARY)
  # previewImg("Otsu Treshold b",img_tresh_b,True)
  # ret_g, img_tresh_g = cv2.threshold(diff_g, 100, 255,cv2.THRESH_BINARY)
  ret_g, img_tresh_g = cv2.threshold(diff_g, 100, 255,cv2.THRESH_BINARY)
  # previewImg("Otsu Treshold g",img_tresh_g,True)
  # ret_r, img_tresh_r = cv2.threshold(diff_r, 100, 255,cv2.THRESH_BINARY)
  ret_r, img_tresh_r = cv2.threshold(diff_r, 100, 255,cv2.THRESH_BINARY)

  # previewImg("Otsu Treshold r",img_tresh_r,True)

  img_tresh_all = img_tresh_b + img_tresh_g + img_tresh_r
  # previewImg("Otsu Treshold all",img_tresh_all, True)

  diff_gray_blur = cv2.GaussianBlur(img_tresh_all,(5,5),0)

  # find otsu's threshold value with OpenCV function
  # ret, img_tresh = cv2.threshold(diff_gray_blur, 60, 255,cv2.THRESH_BINARY)
  ret, img_tresh = cv2.threshold(diff_gray_blur, 0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

  # let's now draw the contour
  arr_cnt, a2 = cv2.findContours(img_tresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

  # let's copy the example image, so we don't paint over it
  img_with_allcontours=img_example.copy()

  cv2.drawContours(img_with_allcontours, arr_cnt, -1, (0,255,0), 3)

  # !!! It may be possible that various contours are showing at this stage, we'll solve that below.
  
  # Just in case, we need to make sure we 'weed out' any contour noise that might generate as images have variations.

  # get the dimensions of the image
  height, width, channels = img_example.shape

  # shorten the variable names
  w=width
  h=height

  validcontours=[]
  contour_index=-1

  # iterate through each contour found
  for i in arr_cnt:

      contour_index=contour_index+1
      ca=cv2.contourArea(i)

      # Calculate W/H Ratio of image
      x,y,w,h = cv2.boundingRect(i)
      aspect_ratio = float(w)/h

      # Flag as edge_noise if the object is at a Corner
      # Contours at the edges of the image are most likely not valid contours
      edge_noise=False
      # if contour starts at x=0 then it's on th edge
      if x==0:
          edge_noise=True
      if y==0:
          edge_noise=True
      # if the contour x value + its contour width exceeds image width, it is on an edge
      if (x+w)==width:
          edge_noise=True
      if (y+h)==height:
          edge_noise=True
              
      # DISCARD noise with measure by area (1x1 round plate dimensions is 1300)
      # if by any chance a contour is drawn on one pixel, this catches it.
      if ca>1300:

          # DISCARD as noise if W/H ratio > 7 to 1 (1x6 plate is 700px to 100px)
          # the conveyor belt has a join line that sometimes is detected as a contour, this ignores it based on w/h ratio
          if aspect_ratio<=6:
              
              # DISCARD if at the Edge
              if edge_noise==False:
                  validcontours.append(contour_index)

  # copy the original picture
  img_withcontours=img_example.copy()
                  
  # call out if more than 1 valid contour is found
  if len(validcontours)>1:
      print("There is more than 1 object in the picture")
  else:
      if len(validcontours)==1:
          print("One object detected")
      else:
          print("No objects detected")
          # FYI: code below will most likely error out as it tries to iterate on an array
      
  # it might be possible we have more than 1 validcontour, iterating through them here
  # if there is zero contours, this most likely will error out
  print('{}번째 레고'.format(index))
  print(validcontours)
  print("===================================================================")
  for k in range(len(validcontours)):
      cv2.drawContours(img_withcontours, arr_cnt,validcontours[k], (0,255,0), 3)
  previewImg('Contours',img_withcontours)

  img_withrectangle=img_example.copy()
  add = 20
  object_position = []
  for j in validcontours:
      x,y,w,h = cv2.boundingRect(arr_cnt[j])
      c_x = x + int(w//2)
      c_y = y + int(h//2)
      n_w = int(w//2)+add
      n_h = int(h//2)+add
      if c_x + n_w < width and c_y + n_h < height and 0 <= c_x - n_w and 0 <= c_y - n_h: 
        if w > h:
            cv2.rectangle(img_withrectangle,(c_x-n_w, c_y-n_w),(c_x+n_w, c_y+n_w),(0,255,0),2)
            object_position.append((c_x-n_w, c_y-n_w, c_x+n_w, c_y+n_w))
        else:
            cv2.rectangle(img_withrectangle,(c_x-n_h, c_y-n_h),(c_x+n_h, c_y+n_h),(0,255,0),2)
            object_position.append((c_x-n_h, c_y-n_h, c_x+n_h, c_y+n_h))
  previewImg('Bounding Rectangle',img_withrectangle)
  for p in object_position:
      try:
        previewImg('cropped object',img_example[p[1]:p[3], p[0]:p[2]])
      except:
        continue
  # if len(object_position) > 0:
  #   previewImg('cropped object',img_example[object_position[-1][1]:object_position[-1][3], object_position[-1][0]:object_position[-1][2]])








```

