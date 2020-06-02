import csv
import pickle
import os
from pathlib import Path

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cur_file = Path(base_path) / "backend" / "crawling" / "data" / "set.p"
print(cur_file)
with open(cur_file, 'rb') as f:
    set_list = pickle.load(f)

mapping_dict = {v["set_num"]: i for i, v in enumerate(set_list, 1)}

f = open('inventories.csv', 'r', encoding='utf-8')
rdr = csv.reader(f)
inventory_dict = dict()
for line in rdr:
    inventory_dict[line[0]] = line[2]
f.close()


print("Loading part data")
cur_file = Path(base_path) / "backend" / "crawling" / "data" / "part.p"
with open(cur_file, 'rb') as f:
    part_list = pickle.load(f)
print("complete")

part_dict = dict()
for part in part_list:
    part_dict[part["part_num"]] = 1

print("Loading color data")
cur_file = Path(base_path) / "backend" / "crawling" / "data" / "color.p"
with open(cur_file, 'rb') as f:
    color_list = pickle.load(f)["results"]
print("complete")
color_dict = dict()
for color in color_list:
    print(color)
    color_dict[color["id"]] = 1
print(color_dict)

# print(inventory_dict)
rows = []
cnt = 0
cnt2 = 0
f = open('inventory_parts.csv', 'r', encoding='utf-8')
rdr = csv.reader(f)
for line in rdr:
    try:
        # inventory_id	part_num	color_id	quantity
        if part_dict.get(line[1]):
            if color_dict.get(int(line[2])):
                line[0] = mapping_dict[inventory_dict[line[0]]]
                line[2] = int(line[2])
                line[3] = int(line[3])
                line.pop()
                rows.append(line)
            else:
                if line[2] != '9999':
                    print(line[2])
    except:
        cnt += 1
        # print("error", line)
        # try:
        #     print(inventory_dict[line[0]])
        #     try:
        #         print(mapping_dict[inventory_dict[line[0]]])
        #     except:
        #         cnt2 += 1
        # except:
        #     pass
f.close()
print(cnt)
print(cnt2)
print(len(rows))
print(rows[0])

with open('setpart.p', 'wb') as f:
    pickle.dump(rows, f)

with open('setpart.p', 'rb') as f:
    setparts = pickle.load(f)
print(len(setparts))
print(setparts[0])




