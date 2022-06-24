import pandas as pd
from matplotlib import pyplot as plt
from os.path import join
import warnings

# upload the file
data_folder = 'validation'
with warnings.catch_warnings(record=True):
    warnings.simplefilter("always")
    df = pd.read_excel(io=join(data_folder, 'export.xlsx'), header=2, usecols=[0, 1, 3], skipfooter=1,
                       engine="openpyxl")

streets = ['Belmont Pier Bicycle Counts', 'Broadway - Eco-Display Classic']

df['month'] = pd.to_datetime(df['Time'], dayfirst=True).dt.to_period('M')
my_df = df.groupby('month').mean()

# my_df['avg'] = my_df[streets].mean(axis=1)

my_df_not_null = my_df[my_df['Broadway - Eco-Display Classic'].notnull()]
print(my_df_not_null)
my_df_not_null['avg'] = my_df_not_null.mean(axis=1)
my_df_not_null.plot(y='avg', figsize=(20, 10))
plt.savefig(fname=join(data_folder, 'figures', 'avg_not_null'))

# visualisation per day and per month

# for street in streets:
#     #     df.plot(x='Time', y=street, figsize=(20, 10))
#     #     plt.savefig(fname=join(data_folder, 'figures', street + '_by_day'))
#     #
#     #
#     my_df.plot(y=street, figsize=(20, 10))
#     plt.savefig(fname=join(data_folder, 'figures', street + '_plot'))

# visualisation of two streets together
