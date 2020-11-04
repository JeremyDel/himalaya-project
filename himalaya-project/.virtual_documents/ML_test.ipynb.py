import pandas as pd
import numpy as np


from members import Members

member = Members().get_data()
member = Members().clean_data(member)


from weather import Weather

weather = Weather().get_data()
weather = Weather().clean_data(weather)


from peaks import Peaks

peak = Peaks().get_data()
peak = Peaks().clean_data(peak)


from expeds import Expeds

exped = Expeds().get_data()
exped = Expeds().clean_data(exped)


print('member', member.shape)
print('peak', peak.shape)
print('exped', exped.shape)


mem_to_drop = ['memb_id',
               'year',
               'unique_id',
                 'peak_id',
                 'residence',
                 'occupation',
                 'summit_claimed',
                 'summit_disputed',
                 'highpt',
                 'high_point',
                 'death',
                 'death_type',
                 'death_height',
                 'death_class',
                 'summit_bid',
                 'summit_term',
               'summit_date1',
               'citizenship'
                ]

member.drop(columns= mem_to_drop, inplace=True)


peak_to_drop = ['peak_name',
                 'pk_name_2',
                 'location',
                 'himal',
                 'region',
                 'open',
                 'unlisted',
                 'trekking',
                 'restrict',
                 'country_status',
                 'year',
                 'season',
                 'expid',
                 'summiter_country',
                 'summiters'
                ]

peak.drop(columns= peak_to_drop, inplace=True)


exp_to_drop = ['year',
                 'season',
                 'route1',
                 'route2',
                 'nation',
                 'leaders',
                 'sponsor',
                 'success1',
                 'success2',
                 'ascent1',
                 'ascent2',
                 'claimed',
                 'disputed',
                 'countries',
               'summit_time',
               'term_date',
               'term_reason',
               'term_note',
               'high_point',
               'traverse',
               'ski',
               'parapente',
               'o2_climb',
               'o2_descent',
               'o2_sleep',
               'o2_medical',
               'o2_taken',
               'o2_unkwn',
               'o2_used',
               'o2_none',
               'other_smts',
               'campsites',
               'accidents',
               'achievment',
               'agency',
               'peak_name',
               'primmem',
               'summiter_deaths',
               'summit_members',
               'summit_hired',
               'hired_deaths'
                ]

exped.drop(columns= exp_to_drop, inplace=True)
exped['summit_date'] = pd.to_datetime(exped.summit_date, errors = 'coerce')
exped['bc_date'] = pd.to_datetime(exped.bc_date , errors = 'coerce')


df = exped.merge(member, on='exp_id', how = 'right')

df = df.set_index('summit_date')
wet = weather.set_index('date_time')

df = df.merge(wet, how='left', left_index=True, right_index=True)

df = df.reset_index()
df.drop(columns=['exp_id', 'index', 'bc_date', 'moonrise', 'moonset', 'sunrise', 'sunset'], inplace = True) 


df.info()


col_num = []
col_bool =[]
col_object =[]

for col in df:
    if df[col].dtype == "float64":
        col_num.append(col)
        
    if df[col].dtype == "int64":
        col_num.append(col)
        
    if df[col].dtype == 'bool':
        col_bool.append(col)
        
    if df[col].dtype == 'object':
        col_object.append(col)
        
col_bool.remove('summit_success')


for col in df:        
    if df[col].dtype == 'bool':
        df[col].fillna(method='bfill')


from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.model_selection import train_test_split, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.impute import SimpleImputer, KNNImputer
from scipy.stats import uniform
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

numeric_transformer = Pipeline(steps=[
    ('imputer', KNNImputer(n_neighbors=2)),
    ('scaler', MinMaxScaler())])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(drop= 'first', handle_unknown='error'))])

# boolean_transformer = Pipeline(steps=[
#     ('imputer', SimpleImputer(strategy='most_frequent'))])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, col_num),
        ('cat', categorical_transformer, col_object)])

# Append classifier to preprocessing pipeline.
# Now we have a full prediction pipeline.
clf = Pipeline(steps=[('preprocessor', preprocessor)])

X = df.drop(columns=['summit_success'])
y = df.summit_success

X_trans = clf.fit_transform(X)


X_train, X_test, y_train, y_test = train_test_split(X_trans, y, test_size=0.3, random_state=42)

model = LogisticRegression(max_iter = 500)
model.fit(X_train, y_train)

print("model score: get_ipython().run_line_magic(".3f"", " % model.score(X_test, y_test))")


from sklearn.metrics import classification_report
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))


## Baseline
y_base = np.zeros(len(y_test))
print(classification_report(y_test, y_base))



