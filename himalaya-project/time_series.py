import os
import pandas as pd
import re

class Time(object):

    def get_data(self):
        """
        This function get the data from the csv file and return a DataFrame.
        """
        root_dir = os.path.abspath('')
        xls_path = os.path.join(root_dir, 'data')
        file_names = [f for f in os.listdir(xls_path) if f.endswith('.csv')]

        def key_from_file_name(f):
            if f[-4:] == '.csv':
                return f[:-4]
        data = {}
        for f in file_names:
            data[key_from_file_name(f)] = pd.read_csv(os.path.join(xls_path, f), sep=';', encoding= 'utf-8')

        data = data['exped_time']

        return data

    def clean_data(self, df):

        df = df.copy()

        ## defining some definitions for the cleaning
        def numbers(x):
            if type(x) == str:
                return int(re.findall(r"\d*", x)[0])
            return x

        def true(x):
            if x == 0:
                return False
            return True

        def no_sponsor(x):
            if x == float('nan'):
                return False
            return x

        def no_route(x):
            if x == float('nan'):
                return 'other'
            return x

        df['term_reason'] = df['term_reason'].map({
            0 : 'Unknown',
            1 : 'Success_main',
            2 : 'Success_sub',
            3 : 'Success_claim',
            4 : 'Bad_weather',
            5 : 'Bad_conditions',
            6 : 'Accident',
            7 : 'Illness',
            8 : 'Lack_sse',
            9 : 'Lack_time',
            10 : 'lack_of_motivation',
            11 : 'no_reach_camp',
            12 : 'no_attempt_climb',
            13 : 'Attempt_rumored',
            14 : "Other"})

        ## Filling with zeros because its makes sense
        df['summit_time'].fillna(0, inplace=True)

        df['season'] = df['season'].map({
                        0 : 'Unknown',
                        1 : 'Spring',
                        2 : 'Summer',
                        3 : 'Autumn',
                        4 : 'Winter'})

        df['host'] =  df['host'].map({
            0 : 'Unknown',
            1 : 'Nepal',
            2 : 'China',
            3 : 'India'})


        return df
