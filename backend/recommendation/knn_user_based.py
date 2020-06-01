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

# ten_review_user_df = pd.DataFrame(CustomUser.objects.all)

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
print(ratings_df)

# reader => 범위 설정  & 학습 부분
reader = Reader(rating_scale=(1, 5))
review_data = surprise.Dataset.load_from_df(df=ratings_df, reader=reader)
trainset = review_data.build_full_trainset()

# knn_gs = cross_validate(KNNBaseline(), review_data, cv=5, n_jobs=5, verbose=False)
# param_grid = {'k': [10, 20, 30, 40, 50, 60]}
# knn_gs = GridSearchCV(KNNBaseline, param_grid, measures=['rmse', 'mae'], cv=5, n_jobs=5)
# knn_gs.fit(review_data)
# print(knn_gs.cv_results)
# print(knn_gs.cv_results['mean_test_rmse'])
# print(knn_gs.cv_results['mean_test_mae'])

# print('학습 시작')
# 피어슨 유사도로 학습
sim_options = {'name': 'pearson', 'user_based': True}
algo = surprise.KNNBaseline(k=30, sim_options=sim_options)
algo.fit(trainset)
# print('학습 완료')

# 작성 안한 레고
def get_unmaked(ratings, store_list, user_id):
    maked_lego_set = ratings[ratings['user_id'] == user_id]['lego_set_id'].tolist()
    unmaked_lego_set = [store for store in store_list if store not in maked_lego_set]
    print('평점 매긴  수 : ', len(maked_lego_set), '추천 대상 레고 세트 수 : ', len(unmaked_lego_set), '전체 레고 세트 수 : ', len(store_list)  )

    return unmaked_lego_set

# 추천 레고세트 정렬해서 리턴
def recomm_lego_set(algo, user_id, unvisited_store, top_n=10):
    predicitons = []
    predicitons = [algo.predict(user_id, kk) for kk in unvisited_store]
    def sortkey_est(pred):
        return pred.est
    
    predicitons.sort(key=sortkey_est, reverse=True)

    top_predictions = predicitons[:top_n]
    top_store_ids = [ int(pred.iid) for pred in top_predictions]
    top_store_rating = [pred.est for pred in top_predictions]
    top_store_preds = [ (id, rating) for id, rating in zip(top_store_ids, top_store_rating) ]

    return top_store_preds

unmaked_lego_set = get_unmaked(ratings_df, ten_lego_set, 32)

top_lego_set_preds = recomm_lego_set(algo, 32, unmaked_lego_set)
print('#### Top 10 레고세트####')
for top_store in top_lego_set_preds:
    print(top_store)

print('결과 툭')






