from matplotlib import pyplot as plt
import pandas as pd
from pandas import DataFrame
from os.path import join


class Validation:
    def __init__(self, folder_data: str, raw_data_path: str):
        self.folder_data = folder_data
        self.raw_data_path = raw_data_path

    def draw_count_time_two_streets(self):
        df = pd.read_csv(join(self.folder_data, self.raw_data_path))
        street = 'Belmont Pier Bicycle Counts'
        # df['date'] = pd.to_datetime(df['Time']).dt.date
        df['month'] = pd.to_datetime(df['Time'], dayfirst=True).dt.to_period('M')
        my_df = df.groupby('month').sum()
        my_df.plot.bar(y=street, figsize=(20, 10))

        plt.savefig(fname=join(self.folder_data, 'figures', street))
