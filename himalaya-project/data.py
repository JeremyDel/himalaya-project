import os
import pandas as pd


class Data:

    def get_data(self):
        """
        This function returns a Python dict.
        Its keys should be 'sellers' 'orders' 'order_items' etc...
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
