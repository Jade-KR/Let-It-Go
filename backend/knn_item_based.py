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

def read_item_names():
    """Read the u.item file from MovieLens 100-k dataset and return two
    mappings to convert raw ids into movie names and movie names into raw ids.
    """

    file_name = get_dataset_dir() + '/ml-100k/ml-100k/u.item'
    rid_to_name = {}
    name_to_rid = {}
    with io.open(file_name, 'r', encoding='ISO-8859-1') as f:
        for line in f:
            line = line.split('|')
            rid_to_name[line[0]] = line[1]
            name_to_rid[line[1]] = line[0]

    return rid_to_name, name_to_rid

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

# k = 10 최적
# knn_gs = cross_validate(KNNBaseline(), review_data, cv=5, n_jobs=5, verbose=False)
# param_grid = {'k': [10, 20, 30, 40, 50, 60]}
# knn_gs = GridSearchCV(KNNBaseline, param_grid, measures=['rmse', 'mae'], cv=5, n_jobs=5)
# knn_gs.fit(review_data)

# 피어슨 유사도로 학습
sim_options = {'name': 'pearson_baseline', 'user_based': False}
algo = surprise.KNNBaseline(k=10, sim_options=sim_options)
algo.fit(trainset)
print('학습 완료')

toy_story_inner_id = algo.trainset.to_inner_iid(1872)
top_neighbors = algo.get_neighbors(toy_story_inner_id, k=10)
print(toy_story_inner_id)
print(top_neighbors)


top_neighbors = [algo.trainset.to_raw_iid(inner_id)
                       for inner_id in top_neighbors]

    
print(dir(top_neighbors))
print(top_neighbors.__getattribute__)
print(top_neighbors)
