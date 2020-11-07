import os
import pandas as pd
import numpy as np
from expeds import Expeds
from members import Members
from peaks import Peaks
from weather import Weather


class Data():

    def get_data(self):
        """
        This function returns a Python dict.
        Its keys should be 'expeds' 'members' 'peaks'
        Its values should be related pandas.DataFrame objects loaded from each csv files
        """

        # Find the absolute path for the root dir (04-Decision-Science)
        # Uses __file__ as absolute path anchor
        root_dir = os.path.abspath('')

        # Use os library for Unix vs. Widowns robustness
        xls_path = os.path.join(root_dir, 'data')

        file_names = [f for f in os.listdir(xls_path) if f.endswith('.xls')]

        def key_from_file_name(f):
            if f[-4:] == '.xls':
                return f[:-4]

        # Create the dictionary
        data = {}
        for f in file_names:
            data[key_from_file_name(f)] = pd.read_excel(os.path.join(xls_path, f))

        return data



    def get_matching_table(self):
        """
        This function returns a DataFrame.
        This DataFrame is a merge between 'peaks', 'members', 'expeds' and 'weather'
        """

        # Get Data
        member = Members().get_data()
        member = Members().clean_data(member)

        weather = Weather().get_data()
        weather = Weather().clean_data(weather)

        exped = Expeds().get_data()
        exped = Expeds().clean_data(exped)

        # Drop columns
        mem_to_drop = ['memb_id','unique_id','peak_id','residence','occupation',
        'summit_claimed','summit_disputed','summit_date1',
        'o2_climb','o2_descent','o2_sleep','o2_medical', 'o2_none',
        'yob', 'route1', 'ascent1', 'leader', 'deputy', 'bconly', 'nottobc', 'support',
        'hired', 'sherpa', 'tibetan']


        exp_to_drop = ['year','season','route1','route2','nation',
        'sponsor','success1','success2', 'ascent1','claimed','disputed',
        'countries','summit_time','term_date','term_note','high_point',
        'traverse','ski','parapente','o2_climb','o2_descent','o2_sleep',
        'o2_medical','o2_taken','o2_unkwn','o2_used','o2_none','other_smts',
        'campsites','accidents','achievment','agency','primmem']

        member.drop(columns= mem_to_drop, inplace=True)
        exped.drop(columns= exp_to_drop, inplace=True)

        exped['summit_date'] = pd.to_datetime(exped.summit_date, errors = 'coerce')
        exped['bc_date'] = pd.to_datetime(exped.bc_date , errors = 'coerce')
        exped = exped.set_index('summit_date')
        weather = weather.set_index('date_time')

        # Feature Engineering (1/2)
        exped['sherpa_ratio'] = exped['tot_hired'] / exped['tot_members']
        exped['sherpa_ratio'] = np.where(exped['sherpa_ratio'] == np.inf, 0, exped['sherpa_ratio'])

        weather['pressure_past'] = weather['pressure'].rolling(window=3).mean()
        weather['pressure_futur'] = weather['pressure'].shift(-2).rolling(window=3).mean()
        weather['stability'] = weather['pressure_futur'] - weather['pressure_past']

        # Merge DataFrames
        df = exped.merge(weather, how='left', left_index=True, right_index=True)
        df = df.reset_index()
        df = df.rename(columns={'index' : 'summit_date'})
        df = df.merge(member, on='exp_id', how = 'right')
        df = df.dropna(subset=['summit_date', 'bc_date'])

        # Feature Engineering (2/2)
        df['cumul_snow'] = 0

        for index, row in df.iterrows():
            date1 = row['bc_date'].date()
            date2 = row['summit_date'].date()
            acc_snow = weather.loc[date1:date2, 'totalSnow_cm'].sum()
            df.loc[index, 'cumul_snow'] = acc_snow

        df.drop(columns=['pressure_past', 'pressure_futur', 'term_reason'], inplace=True)

        return df
