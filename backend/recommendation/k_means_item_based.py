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

from surprise import KNNBaseline
from surprise import Dataset, accuracy, Reader


sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
 'backend.settings')
django.setup()

from api.models import LegoSet, Review, CustomUser, Theme

# # db 모델 변경용 파일 수정
# user_df = pd.DataFrame(CustomUser.objects.all().values("id", "age", "gender"))
# lego_set_df = pd.DataFrame(LegoSet.objects.all().values("id", "name", "theme_id"))

# theme_df = pd.DataFrame(Theme.objects.all().values("id", "parent_id", "name"))
# theme_df['root_id'] = 0

# def get_root_theme(theme_id):
#     root_id = theme_id
#     while(Theme.objects.get(id=root_id).parent_id is not None):
#         root_id = Theme.objects.get(id=root_id).parent_id
#     return root_id

# for i in theme_df.index:
#     theme_df.loc[i, 'root_id'] = get_root_theme(theme_df.loc[i, 'id'])
# theme_df.to_csv('theme.csv')

user_df = pd.DataFrame(CustomUser.objects.all().values("id", "age", "gender"))
theme_df = pd.DataFrame(Theme.objects.all().values("id", "parent_id", "name"))
lego_set_df = pd.DataFrame(LegoSet.objects.all().values("id", "name", "theme_id"))
theme_df = theme_df[theme_df['parent_id'].isna()]

def recoNearLegoSet(temp_id):
    # lego_set_root_theme_id = theme_df.loc[temp_id, 'root_id']    
    lego_set_theme_id = int(lego_set_df[lego_set_df['id'] == temp_id]['theme_id'])
    near_lego_set_df = lego_set_df[lego_set_df['theme_id']== lego_set_theme_id]

    review_df = pd.DataFrame(Review.objects.all().values("user_id", "score", "lego_set_id"))
    review_df = review_df[review_df['lego_set_id'].isin(set(near_lego_set_df['id']))]
    
    review_df = review_df.groupby('lego_set_id').agg(['sum', 'count', 'mean'])['score']
    print(sum(review_df['count']))
    print(review_df)
    if sum(review_df['count']) == 0:
        return list(near_lego_set_df.sample(n=20)['id'])
    else:
        a = sum(review_df['sum'])/sum(review_df['count'])
        min_review = 5

        # 인기도 고려한 평점 계산
        review_df['calc'] = review_df.apply(lambda x: ((x['count']/(x['count']+min_review))*x['mean'] + (min_review/(x['count']+min_review))*a), axis=1)    
        near_lego_set_df = pd.merge(near_lego_set_df[["id", "count"]], review_df["calc"], right_index=True, left_on="id", how='outer').set_index('id')
        near_lego_set_df['calc'] = near_lego_set_df['calc'].fillna(0.0)

        # 카테고리 일치 개수, 인기도 고려한 평점 순 정렬
        near_lego_set_df.sort_values(by=['count', 'calc'], inplace=True, ascending=False)
        return near_lego_set_df.index[:20]

print(recoNearLegoSet(84))



