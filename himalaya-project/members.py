from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
from sklearn.compose import ColumnTransformer
import os
import pandas as pd


data['summit_date1'] = pd.to_datetime(data.summit_date1, errors = 'coerce')
data['death_date'] = pd.to_datetime(data.death_date, errors = 'coerce')

le = LabelEncoder()
data['sex'] = le.fit_transform(data['sex'])

preprocessor = ColumnTransformer([
    ('median', SimpleImputer(strategy='median'), ['yob']),
    ('frequency', SimpleImputer(strategy='most_frequent'), ['citizenship', 'status'])])

# Pass the combined preprocessor into a Pipeline as a single step
final_pipe = Pipeline([('preprocessing', preprocessor)])

tmp = final_pipe.fit_transform(data)
data[['yob', 'citizenship', 'status']] = tmp

data.occupation.fillna('Unknown', inplace = True)
data.residence.fillna('Unknown', inplace = True)
