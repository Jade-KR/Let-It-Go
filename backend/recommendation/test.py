import os
import django
import json
import numpy as np
import pandas as pd
import surprise 
import requests
import sys
from math import sqrt
from surprise.model_selection import cross_validate

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
 'backend.settings')
django.setup()
from surprise import KNNBaseline
from surprise import Dataset, accuracy, Reader
from surprise.model_selection import train_test_split
from surprise.dataset import DatasetAutoFolds
from surprise.model_selection import GridSearchCV
from api.models import Review, CustomUser, Theme

import os
import django
import json
import numpy as np
import pandas as pd
import surprise 
import requests
import sys
from math import sqrt
from surprise.model_selection import cross_validate

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
 'backend.settings')
django.setup()
from surprise import KNNBaseline
from surprise import Dataset, accuracy, Reader
from surprise.model_selection import train_test_split
from surprise.dataset import DatasetAutoFolds
from surprise.model_selection import GridSearchCV
from api.models import Review, CustomUser, Theme, LegoSet

theme_df = pd.DataFrame(Theme.objects.all().values("id", "parent_id", "name"))
lego_set_df = pd.DataFrame(LegoSet.objects.all().values("id", "name", "theme_id"))
theme_df = theme_df[theme_df['parent_id'].isna()]

theme_list = list(theme_df['id'])
theme_dic = {}
for i in theme_list:
    theme_dic[i] = list()

review_df = pd.DataFrame(Review.objects.all().values("user_id", "lego_set_id", "score"))
print('------------------')
# 피클로 테마별 분류?
for i in review_df.index:
    val = review_df.loc[i, 'lego_set_id']
    theme_id = int(lego_set_df.loc[lego_set_df['id'] == val]['theme_id'])
    if theme_id in theme_dic:
        theme_dic[theme_id].append(review_df.loc[i])

for dic in theme_list:
    review_df = pd.DataFrame(theme_dic[dic])
    print(review_df)
    break
    review_df = review_df.groupby('lego_set_id').agg(['sum', 'count', 'mean'])['score']
    # print(sum(review_df['count']))
    # print(review_df)

# def recoNearLegoSet(temp_id):
#     # random으로 20개 추출해주는것
#     if sum(review_df['count']) == 0:
#         return list(near_lego_set_df.sample(n=20)['id'])
#     else:
#         a = sum(review_df['sum'])/sum(review_df['count'])
#         min_review = 5

#         # 인기도 고려한 평점 계산
#         review_df['calc'] = review_df.apply(lambda x: ((x['count']/(x['count']+min_review))*x['mean'] + (min_review/(x['count']+min_review))*a), axis=1)    
#         near_lego_set_df = pd.merge(near_lego_set_df[["id", "count"]], review_df["calc"], right_index=True, left_on="id", how='outer').set_index('id')
#         near_lego_set_df['calc'] = near_lego_set_df['calc'].fillna(0.0)

#         # 카테고리 일치 개수, 인기도 고려한 평점 순 정렬
#         near_lego_set_df.sort_values(by=['count', 'calc'], inplace=True, ascending=False)
#         return near_lego_set_df.index[:20]
        






