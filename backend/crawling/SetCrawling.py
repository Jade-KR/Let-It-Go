import requests
import pickle
API_key = '08d368a0e1830b9fec088091be154133'

headers = {
    'Authorization': 'key ' + API_key,
    'Accept': 'application/json'
}

for i in range(1, 17):
    try:
        with open('set_'+str(i), 'wb') as f:
            a = requests.get(url='https://rebrickable.com/api/v3/lego/sets/?page={}&page_size=1000'.format(i), headers=headers).json()
            pickle.dump(a, f)
    except:
        continue

