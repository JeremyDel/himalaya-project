from datetime import date, datetime
import os
import pandas as pd
import numpy as np
from wwo_hist import retrieve_hist_data

class Weather:

    def get_data_from_wwo(self, frequency=24):
        start_date = '01-JAN-2010'
        end_date = '01-NOV-2020'
        api_key = 'API KEYS!'
        location_list = ['Lobuche']

        hist_weather_data = retrieve_hist_data(api_key,
                                        location_list,
                                        start_date,
                                        end_date,
                                        frequency,
                                        location_label = False,
                                        export_csv = True,
                                        store_df = True)

        data = pd.DataFrame(hist_weather_data[0])
        return data


    def get_data(self):
        """
        This function get the data from the csv file and return a DataFrame.
        """
        root_dir = os.path.abspath('')
        csv_path = os.path.join(root_dir, 'data')
        file_names = [f for f in os.listdir(csv_path) if f.endswith('.csv')]

        for f in file_names:
            if f == 'weather_lobuche.csv':
                data = pd.read_csv(os.path.join(csv_path, f))

        return data

    def clean_data(self, data):
        """
        This function returns a Python DataFrame.
        Clean the DataFrame weather
        """

        # Select the feature in Integer
        feature_int = ['maxtempC', 'mintempC', 'uvIndex', 'moon_illumination',
               'DewPointC', 'FeelsLikeC', 'HeatIndexC', 'WindChillC',
               'WindGustKmph', 'cloudcover', 'humidity', 'pressure',
               'tempC', 'visibility', 'winddirDegree', 'windspeedKmph']

        # Select the feature in Float
        feature_float = ['totalSnow_cm', 'sunHour', 'precipMM']

        # Transform the features in the correct types
        data[feature_int] = data[feature_int].astype(int)
        data[feature_float] = data[feature_float].astype(float)
        data['date_time'] = pd.to_datetime(data['date_time'])

        # Drop the features location
        # Always the same value (Lobuche)
        data = data.drop(columns='location')



        # Propagate last valid observation forward.
        data['moonrise'].replace('No moonrise', np.nan, inplace=True)
        data.ffill(axis=0, inplace=True)

        data['moonset'].replace('No moonset', np.nan, inplace=True)
        data.ffill(axis=0, inplace=True)

        data['sunrise'].replace('No sunrise', np.nan, inplace=True)
        data.ffill(axis=0, inplace=True)

        data['sunset'].replace('No sunset', np.nan, inplace=True)
        data.ffill(axis=0, inplace=True)

        # Convert the feature date_time to date and in string
        date_time_str = data['date_time'].dt.strftime('%Y-%m-%d')

        # Convert the this 4 features to date_time
        # "moonrise", "moonset", "sunrise", "sunset"
        data['moonrise'] = pd.to_datetime(date_time_str + " " + data['moonrise'])
        data['moonset'] = pd.to_datetime(date_time_str + " " + data['moonset'])
        data['sunrise'] = pd.to_datetime(date_time_str + " " + data['sunrise'])
        data['sunset'] = pd.to_datetime(date_time_str + " " + data['sunset'])

        Y = 2000 # dummy leap year to allow input X-02-29 (leap day)
        seasons = [('Winter', (date(Y,  1,  1),  date(Y,  3, 20))),
                   ('Spring', (date(Y,  3, 21),  date(Y,  6, 20))),
                   ('Summer', (date(Y,  6, 21),  date(Y,  9, 22))),
                   ('Autumn', (date(Y,  9, 23),  date(Y, 12, 20))),
                   ('Winter', (date(Y, 12, 21),  date(Y, 12, 31)))]

        def get_season(now):
            if isinstance(now, datetime):
                now = now.date()
            now = now.replace(year=Y)
            return next(season for season, (start, end) in seasons
                        if start <= now <= end)

        data['date_season'] = ''
        data['date_season'] = data['date_time'].apply(lambda x: get_season(x))

        return data

if __name__ == "__main__":
    weather_clean =  Weather().get_data()
    weather_clean = Weather().clean_data(weather_clean)
    root_dir = os.path.abspath('')
    to_data = os.path.join(root_dir, 'data','clean')
    to_path= os.path.join(to_data, 'clean')
    weather_clean.to_csv(to_data+'weather_clean.csv')
