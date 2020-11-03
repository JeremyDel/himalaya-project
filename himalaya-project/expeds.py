import os
import pandas as pd
import re

class Expeds(object):

    def get_data(self):
        """
        This function get the data from the csv file and return a DataFrame.
        """
        root_dir = os.path.abspath('')
        xls_path = os.path.join(root_dir, 'data')
        file_names = [f for f in os.listdir(xls_path) if f.endswith('.xls')]

        def key_from_file_name(f):
            if f[-4:] == '.xls':
                return f[:-4]
        data = {}
        for f in file_names:
            data[key_from_file_name(f)] = pd.read_excel(os.path.join(xls_path, f))

        data = data['expeds']

        return data

    def clean_data(self, df):

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


        ## Applying functions to the specific columns    
        df['ascent1'].fillna(0, inplace=True)
        df['ascent1'] = df['ascent1'].map(numbers)

        df['route1'].fillna('other', inplace = True)
        df['route2'].fillna('other', inplace = True)

        df['achievment'].fillna(0, inplace=True)
        df['achievment'] = df['achievment'].map(true)

        df['sponsor'] = df['sponsor'].map(no_sponsor)
        df['agency'] = df['agency'].map(no_sponsor)

        df['term_note'] = df['term_note'].map({
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


        ## dropping 
        df.drop(columns=['route3', 'route4', 
        'ascent3', 
        'ascent4', 
        'ascent3',
        'approach', 
        'primref', 
        'primid',
        'chksum', 
        'success3',
        'success4'],  inplace = True)
        
        ## Filling with zeros because its makes sense
        df['summit_time'].fillna(0, inplace=True)
        df['other_smts'].fillna(0, inplace=True)

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

if __name__ == "__main__":
    expeds_clean =  Expeds().get_data()
    expeds_clean = Expeds().clean_data(expeds_clean)
    root_dir = os.path.abspath('')
    to_data = os.path.join(root_dir, 'data','clean')
    to_path= os.path.join(to_data, 'clean')
    expeds_clean.to_csv(to_data+'expeds_clean.csv')