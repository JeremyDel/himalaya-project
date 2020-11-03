from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
import datetime
import os
import pandas as pd

class Peaks:

    def get_data(self):
        """
        This  function get the data from the csv file and return a DataFrame.
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

        data = data['peaks']
        return data

    def clean_data(self, df):
        data = df.copy()

        col_to_drop = ['summit_note',
                        'trekyear',
                        'height_f',
                        'summit_date']

        data.drop(columns= col_to_drop, inplace = True)

        data['year'] = data.year.fillna(0)
        data['year'] = data.year.astype(int)

        data['himal'] = data['himal'].map({
                        0 : 'Unclassified',
                        1 : 'Annapurna',
                        2 : 'Api/Byas Risi/Guras',
                        3 : 'Damodar',
                        4 : 'Dhaulagiri',
                        5 : 'Ganesh/Shringi',
                        6 : 'Janak/Ohmi Kangri',
                        7 : 'Jongsang',
                        8 : 'Jugal',
                        9 : 'Kangchenjunga/Simhalila',
                        10 : 'Kanjiroba',
                        11 : 'Kanti/Palchung',
                        12 : 'Khumbu',
                        13 : 'Langtang',
                        14 : 'Makalu',
                        15 : 'Manaslu/Mansiri',
                        16 : 'Mukut/Mustang',
                        17 : 'Nalakankar/Chandi/Changla',
                        18 : 'Peri',
                        19 : 'Rolwaling',
                        20 : 'Saipal'})

        data['region'] = data['region'].map({
                        0 : 'Unclassified',
                        1 : 'Kangchenjunga-Janak',
                        2 : 'Khumbu-Rolwaling-Makalu',
                        3 : 'Langtang-Jugal',
                        4 : 'Manaslu-Ganesh',
                        5 : 'Annapurna-Damodar-Peri',
                        6 : 'Dhaulagiri-Mukut',
                        7 : 'Kanjiroba-Far West'})

        data['country_host'] = data['country_host'].map({
                        0 : 'Unclassified',
                        1 : 'Nepal only',
                        2 : 'China only',
                        3 : 'India only',
                        4 : 'Nepal & China',
                        5 : 'Nepal & India',
                        6 : 'Nepal, China & India'})

        data['country_status'] = data['country_status'].map({
                        0 : 'Unknown',
                        1 : 'Unclimbed',
                        2 : 'Climbed'})

        data['season'] = data['season'].map({
                        0 : 'Unknown',
                        1 : 'Spring',
                        2 : 'Summer',
                        3 : 'Autumn',
                        4 : 'Winter'})


        return data
if __name__ == "__main__":
    peaks_clean =  Peaks().get_data()
    peaks_clean = Peaks().clean_data(peaks_clean)
    root_dir = os.path.abspath('')
    to_data = os.path.join(root_dir, 'data','clean')
    to_path= os.path.join(to_data, 'clean')
    peaks_clean.to_csv(to_data+'peaks_clean.csv')