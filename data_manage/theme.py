import csv
import pickle
import os
from pathlib import Path

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cur_file = Path(base_path) / "backend" / "crawling" / "data" / "theme.p"
print(cur_file)
with open(cur_file, 'rb') as f:
    theme_list = pickle.load(f)


f = open("theme.csv", 'r', encoding='utf-8')
rdr = csv.reader(f)
i = 0
print(len(theme_list))
print(theme_list)
# for line in rdr:
#     # theme_list[i]["root_id"] = int(line[3])
#     # i += 1
#     line[0] = int(line[0])
#     line[1] = int(line[1])
#     line[3] = int(line[3])
#     print(line)

# with open(cur_file, 'wb') as f:
#     pickle.dump(theme_list, f)
# print(theme_list)
# print(i)
# print(rdr)
# for line in rdr:
#     inventory_dict[line[0]] = line[2]
# f.close()
# with open("theme.csv", 'rb') as f:
#     theme_list2 = pickle.load(f)

# print(theme_list)

# print(theme_list2)