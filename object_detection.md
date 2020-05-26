# Object Detection

openCV

Yolo, R-CNN, faster R-CNN...



yolo를 안쓰고 객체 디텍션하는 방법

yolo에서 객체 디텍션하는 부분만 찾아서 하는 방법

yolo를 사용해서 객체 인식까지 하는 방법 



```python
import cv2
import numpy as np
import os
from matplotlib import pyplot as plt
```

```python
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
```

```python
#load the example.  It is a white piece, the most difficult to detect!
img_example=cv2.imread('gdrive/My Drive/Colab Notebooks/input/2_Plate_1x1_Round_180711191345-1.jpg')

#load a background, so we can extract it and make it easy to detect the object.
img_bg=cv2.imread('gdrive/My Drive/Colab Notebooks/input/background_backlit_A.jpg')
```

```python
# our starting Point
previewImg('Background Image',img_bg)
previewImg('Example Image',img_example)
```

```python
# Background - Gray
img_bg_gray=cv2.cvtColor(img_bg, cv2.COLOR_BGR2GRAY)
previewImg("Background Gray",img_bg_gray,True)
# Image - Gray
img_gray=cv2.cvtColor(img_example, cv2.COLOR_BGR2GRAY)
previewImg("Image Gray",img_gray,True)
```

```python
# Calculate Difference
diff_gray=cv2.absdiff(img_bg_gray,img_gray)
previewImg("Pre-Diff",diff_gray,True)
```

```python
# Diff Blur
diff_gray_blur = cv2.GaussianBlur(diff_gray,(5,5),0)
previewImg("Pre-Diff Blur",diff_gray_blur,True)
```

```python
# find otsu's threshold value with OpenCV function
ret, img_tresh = cv2.threshold(diff_gray_blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
previewImg("Otsu Treshold",img_tresh,True)
```

```python
# let's now draw the contour
arr_cnt, a2 = cv2.findContours(img_tresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

# let's copy the example image, so we don't paint over it
img_with_allcontours=img_example.copy()

cv2.drawContours(img_with_allcontours, arr_cnt, -1, (0,255,0), 3)
previewImg('Contours',img_with_allcontours)

# !!! It may be possible that various contours are showing at this stage, we'll solve that below.
```

```python
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
for i in validcontours:                           
    cv2.drawContours(img_withcontours, arr_cnt,validcontours[i], (0,255,0), 3)
previewImg('Contours',img_withcontours)
```

```python
img_withrectangle=img_example.copy()
add = 5
object_position = []
for i in validcontours:
    x,y,w,h = cv2.boundingRect(arr_cnt[i])
    c_x = x + int(w//2)
    c_y = y + int(h//2)
    n_w = int(w//2)+add
    n_h = int(h//2)+add
    if w > h:
        cv2.rectangle(img_withrectangle,(c_x-n_w, c_y-n_w),(c_x+n_w, c_y+n_w),(0,255,0),2)
        object_position.append((c_x-n_w, c_y-n_w, c_x+n_w, c_y+n_w))
    else:
        cv2.rectangle(img_withrectangle,(c_x-n_h, c_y-n_h),(c_x+n_h, c_y+n_h),(0,255,0),2)
        object_position.append((c_x-n_h, c_y-n_h, c_x+n_h, c_y+n_h))
previewImg('Bounding Rectangle',img_withrectangle)
for p in object_position:
    previewImg('cropped object',img_example[p[1]:p[3], p[0]:p[2]])
```





