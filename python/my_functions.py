import os
import glob
import zipfile
import pandas as pd
from pandas import DataFrame
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn import tree
from matplotlib import pyplot as plt

SIGN_0 = '_'


def unzip(path_to_years):
    """
    The method extracts all files from the zip files in the folders
    :param path_to_years: every year should be stored in new folder in which folder named ''zip_files'
    with all the zip file to extract.
    """
    for folder in os.listdir(path_to_years):
        print('_{}'.format(folder))
        new_location = os.path.join(path_to_years, folder)
        zip_loc = os.path.join(new_location, 'zip_files')
        paths = glob.glob(os.path.join(zip_loc, '*.zip'))
        for file_zip in paths:
            with zipfile.ZipFile(file_zip, 'r') as zip_ref:
                zip_ref.extractall(new_location)


def prepare_street_light_data(path_to_years: str, sl_user: str) -> DataFrame:
    """
    It is created tables that store the number of users for each month in each year for each location
    :param path_to_years: The location of the data divided by month
    :param sl_user: streetlight user (bike,ped,vehicles)
    :return:
    """
    res_df = DataFrame()
    # the relevant file for each year for each month is  '*za_' + sl_user + '.csv'
    for month in glob.glob(os.path.join(path_to_years, '*', '[0-9]*')):
        month_name = month.split('\\')[-1].split('_', 1)[-1]
        print('_{}'.format(month_name))
        file_path = glob.glob(os.path.join(month, '*za_' + sl_user + '.csv'))[0]
        temp_pd = pd.read_csv(file_path)
        # Since streetlights have a fixed way of storing data, the code can find the relevant information
        all_day = temp_pd[
            (temp_pd['Day Type'] == '0: All Days (M-Su)') & (temp_pd['Day Part'] == '0: All Day (12am-12am)')]
        # all days include two rows one for trip start and the second one for trip end,
        # so the code select the maximum between them
        rep_place = all_day.groupby('Zone Name').max()
        final_data = rep_place['Average Daily Zone Traffic (StL Index)'].to_dict()
        res_df = pd.concat(objs=[res_df, DataFrame(final_data, index=[month_name])])
    return res_df


def update_file_street_light(file: str) -> DataFrame:
    """
    The date format in @file is updated. As an example, Jan_18_w becomes 2018_01
    :param file:
    :return:
    """
    data_convert = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07',
                    'Aug': '08',
                    'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
    df = pd.read_csv(file)
    df['date'] = df['Unnamed: 0'].apply(
        lambda x: x.replace(x, '20' + x.split('_')[1] + '_' + data_convert[x.split('_')[0]]))
    df.drop('Unnamed: 0', axis='columns', inplace=True)
    # Update the columns name with '_streetlight'
    df.rename(columns={str(col): str(col) + '_streetlight' for col in df.columns[:-1]}, inplace=True)
    return df.set_index('date')


def merge_strava_sl(folder_strava: str, file_sl: DataFrame):
    """
    It takes the strava files and merge it to street lite file based on the data
    :param folder_strava:
    :param file_sl:
    :return:
    """
    file_sl.set_index('date', inplace=True)
    for file in glob.glob(os.path.join(folder_strava, '*')):
        loc_name = file.split('\\')[-1].split('.')[0]
        print(SIGN_0 + loc_name)
        df = pd.read_csv(file).set_index('date')
        file_sl[loc_name + '_strava'] = df['count']
    return file_sl


def draw_results(data_to_draw: DataFrame, tuples_to_draw: list, rank_name=''):
    """
    In this method, counting for each method over time is plotted for each city
    :param data_to_draw:
    :param tuples_to_draw: for example [[('LongBeach_streetlight', 'LongBeach_strava'),
     ('SanLuisObispo_streetlight', 'SanLuisObispo_strava')]
    :return:
    """
    plt.close("all")
    for city in tuples_to_draw:
        city_name = city[0].split('_')[0] + rank_name + '.png'
        y = [city[0], city[1]]
        data_to_draw.plot(x='date', y=y)
        plt.savefig(fname=os.path.join('walking_index/figures', city_name))


def draw_results_ranking(data_to_draw: DataFrame, tuples_to_draw: list):
    """
    The method finds the rank for each counting method and draws the ranking results with the draw_results method
    :param data_to_draw:
    :param tuples_to_draw:
    :return:
    """
    from scipy.stats import rankdata

    new_df = DataFrame()
    new_df['date'] = data_to_draw['date']

    def ranking():
        """
        In order to calculate ranking for many columns the data sho
        :return:
        """
        group = data_to_draw[group_names]
        group_np = group.to_numpy()
        group_rank = rankdata(group_np)
        group_right_fr = np.reshape(group_rank, (data_to_draw.shape[0], len(tuples_to_draw)))
        return group_right_fr

    group_names = [i[0] for i in tuples_to_draw]
    new_df[group_names] = ranking()
    group_names = [i[1] for i in tuples_to_draw]
    new_df[group_names] = ranking()

    draw_results(new_df, tuples_to_draw, '_rank')
    return new_df


def calculate_count_bikes(my_data: DataFrame, clf) -> DataFrame:
    """
    rank bikes count based on the @my_data and the machine learning algorithm
    :param my_data:
    :param clf:
    :return:
    """
    x = my_data[my_data.columns[:-2]].to_numpy()
    y = my_data[my_data.columns[-1]].to_numpy()
    res = DataFrame()
    for i in range(20):
        clf.fit(x, y)
        y_pre = clf.predict(x)
        res[i] = y_pre
        print(clf.score(x, y))
        tree.plot_tree(clf.estimators_[0])
        plt.show()

        # Optional prints
        # print(clf.feature_importances_)
        # print(clf.oob_score_)
        # print(clf.oob_prediction_)
        break
    res['avg'] = res.mean(axis=1)
    res['std'] = res.std(axis=1)

    return res


def calculate_avg_std(my_data: DataFrame, tuples_to_draw: list):
    for


def div_to_walking_count(my_div: tuple):
    """
    Prepare a CSV file with month and count
    :param my_div:
    :return:
    """
    place = my_div[0]
    data = my_div[1]
    print('_{}'.format(place))
    new_data_set = {}
    # Based on Strava's structure, the data is extracted
    split_date = data.split('-')
    new_data_set['date'] = list(map(lambda x, y: '_'.join([x[-4:], y]), split_date[::2], split_date[1::2]))
    new_data_set['count'] = [int(item.split(',')[0]) for item in data.split('total_activities&quot;:')[1:]]
    DataFrame(new_data_set).to_csv(os.path.join('walking_index', 'strava', place + '.csv'))
