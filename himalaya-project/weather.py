import datetime
import os
import pandas as pd
from wwo_hist import retrieve_hist_data

class Weather:
    """
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
        print(xls_path + "/weather_lobuche.csv")"""



    def clean_data(self, data):
        """
        This function returns a Python DataFrame.
        Clean the DataFrame weather
        """

        feature_int = ['maxtempC', 'mintempC', 'uvIndex', 'moon_illumination',
               'DewPointC', 'FeelsLikeC', 'HeatIndexC', 'WindChillC',
               'WindGustKmph', 'cloudcover', 'humidity', 'pressure',
               'tempC', 'visibility', 'winddirDegree', 'windspeedKmph']

        feature_float = ['totalSnow_cm', 'sunHour', 'precipMM']

        data[feature_int] = data[feature_int].astype(int)
        data[feature_float] = data[feature_float].astype(float)
        data['date_time'] = pd.to_datetime(data['date_time'])

        data = data.drop(columns='location')

        date_time_str = data['date_time'].dt.strftime('%Y-%m-%d')

        tab = []
        for i in range(len(data)):
            if data.iloc[i]['moonrise'] == 'No moonrise':
                tab.append(tab[-1])
            else:
                tab.append(data.iloc[i]['moonrise'])

        data['moonrise'] = tab


        tab = []
        for i in range(len(data)):
            if data.iloc[i]['moonset'] == 'No moonset':
                tab.append(tab[-1])
            else:
                tab.append(data.iloc[i]['moonset'])

        data['moonset'] = tab



        data['moonrise'] = pd.to_datetime(date_time_str + " " + data['moonrise'])
        data['moonset'] = pd.to_datetime(date_time_str + " " + data['moonset'])
        data['sunrise'] = pd.to_datetime(date_time_str + " " + data['sunrise'])
        data['sunset'] = pd.to_datetime(date_time_str + " " + data['sunset'])

        return data
