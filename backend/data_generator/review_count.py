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

user_df = pd.DataFrame(CustomUser.objects.all().values("id", "password", "last_login", "is_superuser", "username", "first_name", "last_name", "email", "is_staff" , "is_active", "date_joined", "nickname", "image", "comment", "age", "gender", "review_count", "categories"))
lego_set_df = pd.DataFrame(LegoSet.objects.all().values("id", "name", "num_parts", "images", "description", "tags", "created_at", "updated_at", "theme_id", "user_id", "review_count", "like_count"))
review_df = pd.DataFrame(Review.objects.all().values("user_id","lego_set_id"))

review_df_by_user = review_df.groupby('user_id').count()
review_df_by_lego_set = review_df.groupby('lego_set_id').count()

for i, row in review_df_by_user.iterrows():
    user_df.loc[user_df['id']==i, 'review_count'] = int(row.lego_set_id)
for i, row in review_df_by_lego_set.iterrows():
    lego_set_df.loc[lego_set_df['id']==i, 'review_count'] = int(row.user_id)

user_df.to_csv('user.csv')
lego_set_df.to_csv('lego_set.csv')