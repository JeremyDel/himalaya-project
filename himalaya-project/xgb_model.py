import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.impute import SimpleImputer
from xgboost import XGBClassifier
from members import Members
from weather import Weather
from expeds import Expeds
import joblib
import os
from pickle import dump, load

class HimalXGB():

    def train_model(self):
        """
        This function get the data from csv files and return a trained model.
        It also save the model under the name XGB_model.joblib
        """
        # Get Data
        member = Members().get_data()
        member = Members().clean_data(member)

        weather = Weather().get_data()
        weather = Weather().clean_data(weather)

        exped = Expeds().get_data()
        exped = Expeds().clean_data(exped)

        # Drop columns
        mem_to_drop = ['memb_id','year','unique_id','peak_id','residence','occupation',
        'summit_claimed','summit_disputed','highpt','high_point','death','death_type',
        'death_height','death_class','summit_bid','summit_term','summit_date1',
        'citizenship','o2_climb','o2_descent','o2_sleep','o2_medical', 'o2_none',
        'yob', 'route1', 'ascent1', 'leader', 'deputy', 'bconly', 'nottobc', 'support',
        'hired', 'sherpa', 'tibetan']


        exp_to_drop = ['year','season','route1','route2','nation','leaders',
        'sponsor','success1','success2', 'ascent1','claimed','disputed',
        'countries','summit_time','term_date','term_note','high_point',
        'traverse','ski','parapente','o2_climb','o2_descent','o2_sleep',
        'o2_medical','o2_taken','o2_unkwn','o2_used','o2_none','other_smts',
        'campsites','accidents','achievment','agency','peak_name','primmem',
        'summiter_deaths','summit_members','summit_hired','hired_deaths']

        member.drop(columns= mem_to_drop, inplace=True)
        exped.drop(columns= exp_to_drop, inplace=True)

        exped['summit_date'] = pd.to_datetime(exped.summit_date, errors = 'coerce')
        exped['bc_date'] = pd.to_datetime(exped.bc_date , errors = 'coerce')
        exped['rope'] = np.where(exped['rope']>0, True, False)

        weather['pressure_past'] = weather['pressure'].rolling(window=3).mean()
        weather['pressure_futur'] = weather['pressure'].shift(-2).rolling(window=3).mean()
        weather['stability'] = weather['pressure_futur'] - weather['pressure_past']

        exped['sherpa_ratio'] = exped['tot_hired'] / exped['tot_members']
        exped['sherpa_ratio'] = np.where(exped['sherpa_ratio'] == np.inf, 0, exped['sherpa_ratio'])

        exped = exped.set_index('summit_date')
        weather = weather.set_index('date_time')

        # Merge DataFrames
        df = exped.merge(weather, how='left', left_index=True, right_index=True)
        df = df.reset_index()
        df = df.rename(columns={'index' : 'summit_date'})
        df = df.merge(member, on='exp_id', how = 'right')
        df.drop(columns=['moonrise', 'moonset', 'sunrise', 'sunset'], inplace = True)
        df = df.dropna(subset=['summit_date', 'bc_date'])

        # Feature Engineering
        df['cumul_snow'] = 0

        for index, row in df.iterrows():
            date1 = row['bc_date'].date()
            date2 = row['summit_date'].date()
            acc_snow = weather.loc[date1:date2, 'totalSnow_cm'].sum()
            df.loc[index, 'cumul_snow'] = acc_snow

        feature_to_drop = ['tempC', 'WindChillC', 'primrte', 'disabled',
                   'traverse', 'parapente', 'solo', 'ski', 'speed',
                   'summit_date', 'exp_id', 'bc_date', 'term_reason',
                   'pressure_past', 'pressure_futur', 'uvIndex', 'o2_used']

        df.drop(columns= feature_to_drop, inplace=True)

        # Create an imputer for boolean feature (does nothing)
        class BoolImputer(BaseEstimator, TransformerMixin):
            def __init__(self):
                return None
            def fit(self, X, y=None):
                return self
            def transform(self, X):
                return X

        # Data Processing
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

        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer()),
            ('scaler', MinMaxScaler())])

        bool_transformer = Pipeline(steps=[
            ('imputer', BoolImputer())])

        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(drop= 'first', handle_unknown='error'))])

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, col_num),
                ('bool', bool_transformer, col_bool),
                ('cat', categorical_transformer, col_object)])

        clf = Pipeline(steps=[('preprocessor', preprocessor)])

        X = df.drop(columns=['summit_success'])
        y = df.summit_success

        X_trans = clf.fit_transform(X)
        X_tr = X_trans.toarray()

        X_train, X_test, y_train, y_test = train_test_split(X_tr, y, test_size= 0.3, random_state= 1)

        # get feature names after the pipeline
        ohe_col = list(clf.named_steps['preprocessor'].transformers_[2][1]\
        .named_steps['onehot'].get_feature_names(col_object))

        feature_names = col_num + col_bool + ohe_col

        # Model Traning
        boost = XGBClassifier()
        boost.fit(X_train, y_train)

        # Save trained model
        model_name = 'XGB_model.joblib'
        joblib.dump(boost, model_name)

        return boost

    def load_model(self):
        """
        this function load a trained XGB model.
        """
        loaded_model = joblib.load('XGB_model.joblib')

        return loaded_model

    def predict_model(self, data):
        """
        This function takes a DataFrame and returns a prediction
        """

        df = data.copy()

        # load the pipeline & the model
        model = joblib.load('XGB_model.joblib')

        # scale & impute data
        # Create an imputer for boolean feature (does nothing)
        class BoolImputer(BaseEstimator, TransformerMixin):
            def __init__(self):
                return None
            def fit(self, X, y=None):
                return self
            def transform(self, X):
                return X

        # Data Processing
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


        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer()),
            ('scaler', MinMaxScaler())])

        bool_transformer = Pipeline(steps=[
            ('imputer', BoolImputer())])

        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(drop= 'first', handle_unknown='error'))])

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, col_num),
                ('bool', bool_transformer, col_bool),
                ('cat', categorical_transformer, col_object)])

        clf = Pipeline(steps=[('preprocessor', preprocessor)])


        X = clf.fit_transform(df)
        X_tr = X.toarray()

        y_pred = model.predict(X_tr)

        return y_pred


