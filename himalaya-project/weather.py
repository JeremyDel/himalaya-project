import datetime
import os
import pandas as pd
import numpy as np
from wwo_hist import retrieve_hist_data

class Weather:

    def get_data_from_wwo(self):
        frequency=1
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

    def get_data_from_csv(self):
        # Find the absolute path for the root dir (04-Decision-Science)
        # Uses __file__ as absolute path anchor
        root_dir = os.path.abspath('')

        # Use os library for Unix vs. Widowns robustness
        xls_path = os.path.join(root_dir, 'data')
        print(xls_path + "/weather_lobuche.csv")



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

        return data
