from sklearn.cluster import KMeans
import os
import django
import sys
from django.core.management.base import BaseCommand

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
 'backend.settings')
django.setup()
import numpy as np
import pandas as pd
import requests
from api.models import Review, CustomUser
from backend import settings
import pickle


# user_df = pd.DataFrame(CustomUser.objects.filter(review_count__gte=10))
user_df = pd.DataFrame(CustomUser.objects.all().values("id", "age", "gender"))
male_value = 5
female_value = 0
min_review = 5

# gender 값을 정수로 변환
user_df['gender'] = user_df['gender'].apply(lambda x: 5*x)

# kmeans 학습
kmeans = KMeans(n_clusters=5, init='k-means++', max_iter=300, random_state=0)
kmeans.fit(user_df[["age", "gender"]])
# print('cluster 완료')

# kmeans.labels_ : 몇번 클러스터인지 라벨링 붙이고 분리했었던 id col을 붙임
user_df['cluster'] = kmeans.labels_
review_df = pd.DataFrame(Review.objects.all().values("user_id", "score", "lego_set_id"))
user_df = user_df[user_df['id'].isin(set(review_df['user_id']))]

user_df = user_df.set_index('id')
# 리뷰 테이블에 유저 클러스터정보를 조인해서 합쳐준다.
temp_df = pd.merge(user_df["cluster"], review_df, left_index=True, right_on="user_id")
temp_df["score"] = temp_df["score"].astype(float)

# 클러스터의 인덱스에 클러스터 번호에 해당하는 정보만 가져와서 저장한다.
cluster_list = [temp_df[["lego_set_id", "score"]][temp_df["cluster"]==i] for i in range(5)]

for i in range(5):
    # cluster 각각을 store로 묶는다
    cluster_list[i] = cluster_list[i].groupby('lego_set_id').agg(['sum', 'count', 'mean'])['score']
    cluster_list[i] = cluster_list[i][cluster_list[i]['count']>=5]

    # 각 클러스터별 평균평점을 계산한다.
    a = sum(cluster_list[i]['sum']) / sum(cluster_list[i]['count'])

    # calc 칼럼을 추가하고 거기에 인기도 점수 계산한 값을 넣어준다.
    cluster_list[i]['calc'] = cluster_list[i].apply(lambda x: ((x['count']/(x['count']+min_review))*x['mean'] + (min_review/x['count']+min_review))*a, axis=1)

    # calc 기준으로 내림차순 정렬한다.
    cluster_list[i].sort_values(['calc'], ascending=False, inplace=True)
    cluster_list[i] = cluster_list[i].index

# centroid -> 저쟁해야하는 값
centroid = kmeans.cluster_centers_

with open('k_means_user_based.p', 'wb') as f:
    pickle.dump(cluster_list, f)
    pickle.dump(centroid, f)

with open('k_means_user_based.p', 'rb') as f:
    cluster_list2 = pickle.load(f)
    centroid2 = pickle.load(f)

def get_cluster(centroid, age, gender):

    def gender_to_integer(gender):
        if gender=='남':
            return male_value
        else:
            return female_value

    gtoi = gender_to_integer(gender)

    index = -1
    init_distance = 9999999

    for i in range(5):
        distance_y = centroid[i][0]
        distance_x = centroid[i][1]

        distance = (distance_y-age)*(distance_y-age) + (distance_x-gtoi)*(distance_x-gtoi)
        if(init_distance>distance):
            init_distance = distance
            index = i
    return index

print('----요기')
print(user_df)
print(get_cluster(centroid, 30, '남'))
# 성별과 나이를 받아서 k_means하기 위한 임시값
temp_gender = '남'
temp_age = 47

#
cluster = get_cluster(centroid, temp_age, temp_gender)

def get_Top_stores(cluster, n=10):
    return cluster_list[cluster][:n]

result = get_Top_stores(cluster)
print(result)
