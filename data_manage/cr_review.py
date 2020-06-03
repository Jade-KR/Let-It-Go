import csv
import pickle
import os
from pathlib import Path


f = open('api_review.csv', 'r', encoding='utf-8')
rdr = csv.reader(f)
review_list = []
for line in rdr:
    # id	content	score	created_at	updated_at	user_id	lego_set_id
    # score user_id lego_set_id
    try:
        review_list.append([int(line[2]), int(line[5]), int(line[6])])
    except:
        print(1)

with open('review.p', 'wb') as f:
    pickle.dump(review_list, f)