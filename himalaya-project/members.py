from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
import datetime
import os
import pandas as pd

class Members:

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

        data = data['members']
        return data

    def clean_data(self, df):
        """
        This function takes a DataFrame and returns a clean DataFrame.
        """
        data = df.copy()

        data['unique_id'] = data['exp_id'] + '_' + data['memb_id'].astype(str)

        col_to_drop = ['first_name',
               'last_name',
               'age',
               'birthdate',
               'route2',
               'route3',
               'ascent2',
               'ascent3',
               'summit_time1',
               'summit_time2',
               'summit_time3',
               'summit_date2',
               'summit_date3',
               'o2_note',
               'death_date',
               'death_time',
               'hcn',
               'mchksum']

        data.drop(columns= col_to_drop, inplace = True)

        data['season'] = data['season'].map({
                        0 : 'Unknown',
                        1 : 'Spring',
                        2 : 'Summer',
                        3 : 'Autumn',
                        4 : 'Winter'})

        data['death_type'] = data['death_type'].map({
                        0 : 'Unspecified',
                        1 : 'AMS',
                        2 : 'Exhaustion',
                        3 : 'Exposure / frostbite',
                        4 : 'Fall',
                        5 : 'Crevasse',
                        6 : 'Icefall collapse',
                        7 : 'Avalanche',
                        8 : 'Falling rock / ice',
                        9 : 'Disappearance',
                        10 : 'Illness (non-AMS)',
                        11 : 'Other',
                        12 : 'Unknown'})

        data['death_class'] = data['death_class'].map({
                        0 : 'Unspecified',
                        1 : 'Death enroute BC',
                        2 : 'Death at BC / ABC',
                        3 : 'Route preparation',
                        4 : 'Ascending in summit bid',
                        5 : 'Descending from summit bid',
                        6 : 'Expedition evacuation',
                        7 : 'Other / Unknown'})

        data['summit_bid'] = data['summit_bid'].map({
                        0 : 'Unspecified',
                        1 : 'No summit bid',
                        2 : 'Aborted below high camp',
                        3 : 'Aborted at high camp',
                        4 : 'Aborted above high camp',
                        5 : 'Successful summit bid'})

        data.rename(columns={'summitter' : 'summit_term'}, inplace=True)

        data['summit_term'] = data['summit_term'].map({
                        0 : 'Unspecified',
                        1 : 'Success',
                        2 : 'Success subpeak',
                        3 : 'Bad weather',
                        4 : 'Bad conditions',
                        5 : 'Accident',
                        6 : 'AMS',
                        7 : 'Exhaustion',
                        8 : 'Frostbite',
                        9 : 'Illnesses',
                        10 : 'Logisitic',
                        11 : 'O2 system failure',
                        12 : 'Route difficulty',
                        13 : 'Too late/slow',
                        14 : 'Assisting',
                        15 : 'Route/camp/rope preparation',
                        16 : 'No time left',
                        17 : 'No climbing',
                        18 : 'Other',
                        19 : 'Unknown'})

        data['summit_date1'] = pd.to_datetime(data.summit_date1, errors = 'coerce')

        # Combine "age_transformer" and "One hot encoder" into a single preprocessor
        preprocessor = ColumnTransformer([
            ('median', SimpleImputer(strategy='median'), ['yob']),
            ('frequency', SimpleImputer(strategy='most_frequent'), ['citizenship', 'status']),
            ('ohe', OneHotEncoder(drop= 'first'), ['sex'])])

        # Pass the combined preprocessor into a Pipeline as a single step
        final_pipe = Pipeline([('preprocessing', preprocessor)])

        data_trans = final_pipe.fit_transform(data)

        data[['yob', 'citizenship', 'status', 'sex']] = data_trans

        data.rename(columns={'sex' : 'sex_M'}, inplace=True)

        data.occupation.fillna('Unknown', inplace = True)
        data.residence.fillna('Unknown', inplace = True)

        now_year = datetime.datetime.now().year
        data['age'] = now_year - data['yob']

        return data

        
if __name__ == "__main__":
    members_clean =  Members().get_data()
    members_clean = Members().clean_data(members_clean)
    root_dir = os.path.abspath('')
    to_data = os.path.join(root_dir, 'data', 'clean')
    to_path= os.path.join(to_data, 'clean')
    members_clean.to_csv(to_path+'members_clean.csv')