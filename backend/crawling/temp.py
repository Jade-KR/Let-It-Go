
import pickle
set_list = []
for i in range(1, 17):
    with open('data/temp/set_'+str(i), 'rb') as f:
        set_l = pickle.load(f)
        set_list = set_list + set_l["results"]

with open('set2.p', 'wb') as f:
    pickle.dump(set_list, f)
print(len(set_list))