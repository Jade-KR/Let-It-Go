import csv
import pickle
import os
from pathlib import Path



user_list = []
f = open('user.csv', 'r')
rdr = csv.reader(f)
i = 0
for line in rdr:
    try:
        # 	id	password	last_login	is_superuser	username	first_name	last_name	email	is_staff	is_active	date_joined	nickname	image	comment	age	gender	review_count	categories
        #   id  username    nickname    age gender  review_count
        user_list.append([int(line[1]), line[5], line[5], int(line[15]), int(line[16]), int(line[17])])

    # print(line)
    except:
        pass
    i += 1
f.close()

with open('user.p', 'wb') as f:
    pickle.dump(user_list, f)