import os
from pathlib import Path
import csv

base_dir = "./input2/"
source_dir = "./tempdata/lego-vs-generic-brick-image-recognition/Cropped Images/"
# C:\Users\multicampus\s02p31d108\AI_learning\tempdata\lego-vs-generic-brick-image-recognition
f = open('tempdata/lego-vs-generic-brick-image-recognition/ImageKey.csv', 'r', encoding='utf-8')
lego_images = []
rdr = csv.reader(f)
for line in rdr:
    if line[6] == "Lego" and line[0] == "Cropped Images":
        # print(line)
        # print(source_dir+line[1] + '/' + line[4])
        # print(base_dir + line[7])
        with open(source_dir+line[1] + '/' + line[4], 'rb') as f:
            with open(base_dir + line[7] + '/' + line[4], 'wb') as f2:
                f2.write(f.read())
        print(line)
# f.close()    
# print(dir(os.path.dirname(os.path.abspath(__file__))))
# print(dir(os.path))
# print(os.listdir(Path(os.path.dirname(os.path.abspath(__file__))) / "tempdata"))
# print(os.path.dirname(os.path.abspath(__file__)).index())
# print(Path(os.path.dirname(os.path.abspath(__file__))) / "tempdata")
