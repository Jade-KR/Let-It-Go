import os
import django
import json
import numpy as np
import pandas as pd
import surprise 
import requests
from math import sqrt
from surprise.model_selection import cross_validate

from surprise import KNNBaseline
from surprise import Dataset, accuracy, Reader



os.environ.setdefault('DJANGO_SETTINGS_MODULE',
 'backend.settings')
django.setup()

from api.models import LegoSet, Review, CustomUser, Theme

# user_df = pd.DataFrame(CustomUser.objects.all().values("id", "age", "gender"))
# review_df = pd.DataFrame(Review.objects.all().values("user_id", "score", "lego_set_id"))
# db 모델 변경용 파일 수정
theme_df = pd.DataFrame(Theme.objects.all().values("id", "parent_id", "name"))
theme_df['root_id'] = 0

def get_root_theme(theme_id):
    root_id = theme_id
    while(Theme.objects.get(id=root_id).parent_id is not None):
        root_id = Theme.objects.get(id=root_id).parent_id
    return root_id

for i in theme_df.index:
    theme_df.loc[i, 'root_id'] = get_root_theme(theme_df.loc[i, 'id'])

# theme_df.to_csv('theme.csv')



def recoNearLegoSet(temp_id):
    lego_set_theme_id = get_root_theme(temp_id)
    print(lego_set_theme_id)
    all_lego_set = LegoSet.objects.all()
    list1 = []
    for ls in all_lego_set.iterator():
        ls_root_theme_id = get_root_theme(ls.theme_id)
        if(lego_set_theme_id == ls_root_theme_id):
            list1.append(ls)
    print(list1[0:5])
    print(len(list1))
    # lego_set_df = pd.DataFrame(all_lego_set.values(id, theme_id, review_count, like_count))

    return 1


print(recoNearLegoSet(84))



