import os
import django
import json
import numpy as np
import pandas as pd
import surprise 
import requests
from math import sqrt
from surprise.model_selection import cross_validate

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
review_df = pd.DataFrame(Review.objects.all().values("user_id", "score", "set_id_id"))

# ten_review_user_df = pd.DataFrame(CustomUser.objects.all)

ten_user_df = review_df.groupby("user_id").count()
temp_review_df = review_df.groupby("set_id_id").count()

# 10개 이상의 레고작성글에 대한 것
ten_lego_set = set(temp_review_df[temp_review_df['score']>=10].index)

# 10개 이상의 리뷰를 남긴 user
ten_user_set = set(ten_user_df[ten_user_df["score"]>=10].index)
print('-------')
print(ten_lego_set)
print(ten_user_set)

# 해당 작품에 대한 리뷰가 10개이상이면서 10개 이상 작성자의 정보만 남김
ten_review_df = review_df[review_df['user_id'].isin(ten_user_set)]
ten_review_df = ten_review_df[ten_review_df['set_id_id'].isin(ten_lego_set)]

ratings_df = ten_review_df[['user_id', 'set_id_id', 'score']]
print(ratings_df)

# reader => 범위 설정  & 학습 부분
reader = Reader(rating_scale=(1, 5))
review_data = surprise.Dataset.load_from_df(df=ratings_df, reader=reader)
trainset = review_data.build_full_trainset()

knn_gs = cross_validate(KNNBaseline(), review_data, cv=5, n_jobs=5, verbose=False)
param_grid = {'k': [10, 20, 30, 40, 50, 60]}
knn_gs = GridSearchCV(KNNBaseline, param_grid, measures=['rmse', 'mae'], cv=5, n_jobs=5)
knn_gs.fit(review_data)
print(knn_gs.cv_results)
print(knn_gs.cv_results['mean_test_rmse'])
print(knn_gs.cv_results['mean_test_mae'])
print('학습 시작')
# 피어슨 유사도로 학습
sim_options = {'name': 'pearson', 'user_based': False}
algo = surprise.KNNBaseline(k=30, sim_options=sim_options)
algo.fit(trainset)
print('학습 완료')

top_neighbors = 






