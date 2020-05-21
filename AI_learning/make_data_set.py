import os
from pathlib import Path
import random

print(os.listdir('./input2'))
a = os.listdir('./input2')
cnt = []

for i in range(6):
    cnt1 = 0
    for image in os.listdir('./input2/' + a[i]):
        print('./input2/seg_test/seg_test/' + a[i] + '/' + image)
        # 평가용 이미지 10, 테스트용 이미지 10, 학습용 이미지 80
        r = random.random()
        if r < 0.1:
            # 평가용
            with open('./input2/' + a[i] + '/' + image, 'rb') as f:
                with open('./input2/seg_pred/seg_pred/' + image, 'wb') as f2:
                    f2.write(f.read())
        elif r < 0.2:
            # 테스트용
            with open('./input2/' + a[i] + '/' + image, 'rb') as f:
                with open('./input2/seg_test/seg_test/' + a[i] + '/' + image, 'wb') as f2:
                    f2.write(f.read())
        else:
            # 학습용
            with open('./input2/' + a[i] + '/' + image, 'rb') as f:
                with open('./input2/seg_train/seg_train/' + a[i] + '/' + image, 'wb') as f2:
                    f2.write(f.read())
        cnt1 += 1
    cnt.append(cnt1)

print(os.listdir('./input2'))
print(cnt)
print(dir(random))
for i in range(100):
    print(random.random())