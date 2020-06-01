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

theme_df = pd.DataFrame(Theme.objects.all().values("id", "parent_id", "name"))
theme_df = theme_df[theme_df['parent_id'] is null]
print(theme_df)