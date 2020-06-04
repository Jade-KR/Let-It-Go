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
    review_df = review_df.groupby('lego_set_id').agg(['sum', 'count', 'mean'])['score']
        
