import csv
import pickle
import os
from pathlib import Path

# base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# cur_file = Path(base_path) / "backend" / "crawling" / "data" / "set.p"
# print(cur_file)
# with open(cur_file, 'rb') as f:
#     set_list = pickle.load(f)
# print(set_list)
set_list = []
f = open('lego_set.csv', 'r')
rdr = csv.reader(f)
i = 0
for line in rdr:
    try:
        # theme     name    n  um_parts     images  review_count
        print(line[9], line[2], line[3], line[4], line[11])
        set_list.append([int(line[9]), line[2], int(line[3].split('.')[0]), line[4], int(line[11])])
    # print(line)
    except:
        pass
    i += 1
f.close()


with open('set.p', 'wb') as f:
    pickle.dump(set_list, f)
# print(set_list)


# 	id	name	num_parts	images	description	tags	created_at	updated_at	theme_id	user_id	review_count	like_count
