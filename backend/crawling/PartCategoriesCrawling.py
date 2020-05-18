import requests
import pickle
API_key = '08d368a0e1830b9fec088091be154133'

headers = {
    'Authorization': 'key ' + API_key,
    'Accept': 'application/json'
}

with open('part_categories', 'wb') as f:
    a = requests.get(url='https://rebrickable.com/api/v3/lego/part_categories/?page_size=1000', headers=headers).json()
    pickle.dump(a, f)
print(a)
