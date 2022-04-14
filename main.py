import os
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from python.html import *
from python.my_functions import *

if __name__ == '__main__':
    # PARAMETER SECTION #
    parameters = {'unzip': False, 'prepare_street_light_data': False, 'update_file_street_light': False,
                  'merge_strava_sl': True,
                  'calculate_count_bikes': False,
                  'div_to_walking_count': False}
    # The folder_data path with \\
    FOLDER_DATA = 'walking_index\\streetlight\\by_month'
    # for 'prepare_street_light_data' and 'update_file_street_light'
    RES_LOC = os.path.join(FOLDER_DATA, 'data.csv')
    # for 'prepare_street_light_data'
    SL_USER = 'ped'
    # for 'update_file_street_light' and 'merge_strava_sl'
    COM_FILE = r'walking_index\comparison.csv'
    # for merge_strava_sl
    STRAVA_FOLDER = r'walking_index\strava'

    # END PARAMETER SECTION #

    if parameters['unzip']:
        print('unzip')
        unzip(path_to_years=FOLDER_DATA)

    if parameters['prepare_street_light_data']:
        print('prepare_street_light_data')
        res = prepare_street_light_data(path_to_years=FOLDER_DATA, sl_user=SL_USER)
        res.to_csv(RES_LOC)
    if parameters['update_file_street_light']:
        print('update_file_street_light')
        update_file_street_light(RES_LOC).to_csv(COM_FILE)
    if parameters['merge_strava_sl']:
        print('merge_strava_sl')
        merge_strava_sl(folder_strava=STRAVA_FOLDER, file_sl=pd.read_csv(COM_FILE)).to_csv(
            COM_FILE.replace('comparison', 'final'))
    if parameters['calculate_count_bikes']:
        # Parameters for this
        input_file = 'analysis/ml.csv'
        regressor = RandomForestRegressor(oob_score=True)
        file_output = os.path.join('analysis', str(regressor).split('(')[0] + '10_times.csv')
        is_file_output = False
        print('calculate_count_bikes')
        if is_file_output:
            calculate_count_bikes(my_data=pd.read_csv(input_file), clf=regressor).to_csv(
                file_output)
        else:
            calculate_count_bikes(my_data=pd.read_csv(input_file), clf=regressor)

    if parameters['div_to_walking_count']:
        # Get the pedestrian count for each place for the months between 2018 and 2021.
        # This data is stored as a dictionary of places and HTML elements
        print('div_to_walking_count')
        for my_html in my_dic.items():
            div_to_walking_count(my_html)
