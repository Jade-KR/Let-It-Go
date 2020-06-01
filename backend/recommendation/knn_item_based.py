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
from api.models import Review, CustomUser

user_df = pd.DataFrame(CustomUser.objects.all().values("id", "age", "gender"))
review_df = pd.DataFrame(Review.objects.all().values("user_id", "score", "lego_set_id"))

ten_user_df = review_df.groupby("user_id").count()
temp_review_df = review_df.groupby("lego_set_id").count()

# 10개 이상의 레고작성글에 대한 것
ten_lego_set = set(temp_review_df[temp_review_df['score']>=10].index)

# 10개 이상의 리뷰를 남긴 user
ten_user_set = set(ten_user_df[ten_user_df["score"]>=10].index)

# 해당 작품에 대한 리뷰가 10개이상이면서 10개 이상 작성자의 정보만 남김
ten_review_df = review_df[review_df['user_id'].isin(ten_user_set)]
ten_review_df = ten_review_df[ten_review_df['lego_set_id'].isin(ten_lego_set)]

ratings_df = ten_review_df[['user_id', 'lego_set_id', 'score']]
# print(ratings_df)

# reader => 범위 설정  & 학습 부분
reader = Reader(rating_scale=(1, 5))
review_data = surprise.Dataset.load_from_df(df=ratings_df, reader=reader)
trainset = review_data.build_full_trainset()

# 피어슨 유사도로 학습
sim_options = {'name': 'pearson_baseline', 'user_based': False}
algo = surprise.KNNBaseline(k=10, sim_options=sim_options)
algo.fit(trainset)
# print('학습 완료')

def recoNearLegoSet(temp_id):
    lego_set__inner_id = algo.trainset.to_inner_iid(temp_id)
    top_neighbors = algo.get_neighbors(lego_set__inner_id, k=20)

    top_neighbors = [algo.trainset.to_raw_iid(inner_id) for inner_id in top_neighbors]

    return top_neighbors

print(recoNearLegoSet(1872))

