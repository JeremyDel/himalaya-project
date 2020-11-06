import os
import pandas as pd
from expeds import Expeds
from members import Members
from peaks import Peaks
from weather import Weather


class Data:

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



    def get_match_table(self):
        """
        This function returns a DataFrame.
        This DataFrame is a merge between 'peaks', 'members', 'expeds' and 'weather'
        """

        # Get and clean this 4 tables

        # Get and clean the table 'peak'
        peak = Peaks().get_data()
        peak = Peaks().clean_data(peak)

        # Get and clean the table 'member'
        member = Members().get_data()
        member = Members().clean_data(member)

        # Get and clean the table 'exped'
        exped = Expeds().get_data()
        exped = Expeds().clean_data(exped)

        # Get and clean the table 'weather'
        weather = Weather().get_data()
        weather = Weather().clean_data(weather)

        # Drop some useless features of the table 'member'
        mem_to_drop = ['memb_id',
               'year',
               'unique_id',
                 'peak_id',
                 'residence',
                 'occupation',
                 'summit_claimed',
                 'summit_disputed',
                 'highpt',
                 'high_point',
                 'death',
                 'death_type',
                 'death_height',
                 'death_class',
                 'summit_bid',
                 'summit_term',
               'summit_date1',
               'citizenship'
                ]

        member.drop(columns= mem_to_drop, inplace=True)

        # Drop some useless features of the table 'peak'
        peak_to_drop = ['peak_name',
                 'pk_name_2',
                 'location',
                 'himal',
                 'region',
                 'open',
                 'unlisted',
                 'trekking',
                 'restrict',
                 'country_status',
                 'year',
                 'season',
                 'expid',
                 'summiter_country',
                 'summiters'
                ]

        peak.drop(columns= peak_to_drop, inplace=True)

        # Drop some useless features of the table 'exped'
        exp_to_drop = ['year',
                 'season',
                 'route1',
                 'route2',
                 'nation',
                 'leaders',
                 'sponsor',
                 'success1',
                 'success2',
                 'ascent1',
                 'claimed',
                 'disputed',
                 'countries',
               'summit_time',
               'term_date',
               'term_note',
               'high_point',
               'traverse',
               'ski',
               'parapente',
               'o2_climb',
               'o2_descent',
               'o2_sleep',
               'o2_medical',
               'o2_taken',
               'o2_unkwn',
               'o2_used',
               'o2_none',
               'other_smts',
               'campsites',
               'accidents',
               'achievment',
               'agency',
               'peak_name',
               'primmem',
               'summiter_deaths',
               'summit_members',
               'summit_hired',
               'hired_deaths'
                ]

        exped.drop(columns= exp_to_drop, inplace=True)

        # Change the type of the date in the table 'exped'
        exped['summit_date'] = pd.to_datetime(exped.summit_date, errors = 'coerce')
        exped['summit_date1'] = exped['summit_date']
        exped['bc_date'] = pd.to_datetime(exped.bc_date , errors = 'coerce')

        ## Merging
        # Merge the table 'exped' with the table 'member'
        df = exped.merge(member, on='exp_id', how = 'right')

        # Set the index of the table 'merging_table and weather'
        df = df.set_index('summit_date')
        wet = weather.set_index('date_time')

        # Merge the table 'exped-member' and 'weather'
        df = df.merge(wet, how='left', left_index=True, right_index=True)
        df = df.reset_index()
        
        df.drop(columns=['index', 'moonrise', 'moonset', 'sunrise', 'sunset'], inplace = True)

        df = df.merge(peak, on='peak_id', how='left')

        return df