import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from expeds import Expeds
import pmdarima as pm



# Get Data
exped = Expeds().get_data()
exped = Expeds().clean_data(exped)

root_dir = os.path.abspath('')
xls_path = os.path.join(root_dir, 'data\\exped_time_2.xls')
time = pd.read_excel(xls_path)

# Drop columns
exp_to_drop = ['year','season','route1','route2','nation','leaders','sponsor','success1','success2',
               'ascent1','claimed','disputed','countries','summit_time','term_date','term_reason', 'summit_days',
               'term_note','high_point','traverse','ski','parapente','o2_climb','o2_descent','o2_sleep','o2_medical',
               'o2_taken','o2_unkwn','o2_used','o2_none','other_smts','campsites','accidents','achievment','agency',
               'peak_name','primmem','summiter_deaths','summit_hired','hired_deaths']

exped.drop(columns= exp_to_drop, inplace=True)

exped['summit_date'] = pd.to_datetime(exped.summit_date, errors = 'coerce')
exped['bc_date'] = pd.to_datetime(exped.bc_date , errors = 'coerce')

# Merge DataFrame
df = time[time['peakid']=='EVER']
df.drop(['peakid'], axis=1, inplace=True)
df['smtdate'] = pd.to_datetime(df.smtdate, errors = 'coerce')

# Create DataFrame
df_ts = df.dropna()
df_ts.set_index('smtdate', inplace=True)
df_ts = df_ts.groupby(['smtdate']).sum(['smtmembers'])
df_ts = df_ts.asfreq('d')
df_ts = df_ts.fillna(0)
df_ts = df_ts[df_ts.index >= '1960']

# Create DataFrame with only month = May
df_ts = df_ts.drop(columns=[
                 'year',
                 'season',
                 'host',
                 'success1',
                 'termreason',
                'mdeaths',
                 'heightm',
                'smthired',
                 'hdeaths',
                'totdays'])

df_ts['month'] = df_ts.index.month
df_ts['year'] = df_ts.index.year
df_ts_may = df_ts[df_ts['month']==5]
df_ts_may = df_ts_may.groupby(['year']).agg({'smtdays' : 'mean',
                                'camps' : 'mean',
                                'rope' : 'mean',
                                'totmembers' : 'sum',
                                'smtmembers' : 'sum',
                                'tothired' : 'mean'})

date_rng = pd.date_range(start='1960', end='2020', freq='A-MAY')
df = pd.DataFrame(date_rng, columns=['date'])
df = df.set_index(df.date.dt.year)
df = df.merge(df_ts_may, how='left', left_index=True, right_index=True)
df = df.set_index('date')
df = df.asfreq('A-MAY')
df.loc['2014', 'smtmembers'] = int(df.loc['2013', 'smtmembers'])
df.loc['2015', 'smtmembers'] = (int(df.loc['2014', 'smtmembers']) + int(df.loc['2016', 'smtmembers']))/2
df['smtmembers_shift'] = df['smtmembers'] - df['smtmembers'].shift(1)
df = df.dropna()

# Create time series
ts = df.smtmembers

# Train model
train = ts[:'2010']
test = ts['2011':]

sarima = pm.auto_arima(train,
                      start_p=0,
                      start_q=0,
                      test='adf',
                      max_p=3,
                      max_q=3,
                      m=12,
                      d=None,
                      seasonal=True,
                      start_P=0,
                      D=1,
                      trace=True,
                      error_action='ignore',
                      suppress_warnings=True,
                      stepwise=True)

# Predict
ypred = sarima.predict(len(test))
