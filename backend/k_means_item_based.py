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
from surprise import SVD, Dataset, accuracy, Reader
from surprise.model_selection import train_test_split
from surprise.dataset import DatasetAutoFolds
from surprise.model_selection import GridSearchCV
from math import acos, cos, sin, radians

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
 'backend.settings')
django.setup()

from api.models import LegoSet, Review, CustomUser, Theme

def get_root_theme(theme_id):
    root_id = theme_id
    while(Theme.objects.get(id=root_id).parent_id is not None):
        root_id = Theme.objects.get(id=root_id).parent_id
    return root_id

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


recoNearLegoSet(84)



