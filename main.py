import os
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from python.html import *
from python.my_functions import *
from python.validation import *

if __name__ == '__main__':

    # PARAMETER SECTION #
    parameters = {'main': [False, {'div_to_count': False,
                                   'unzip': False, 'prepare_street_light_data': False,
                                   'update_file_street_light': False,
                                   'merge_strava_sl': False,
                                   'draw_results': False,
                                   'draw_results_method': False,
                                   'calculate_avg_std': False,
                                   'calculate_count_ml': False}],
                  'validation': [True, {'draw_count_time_two_streets': True}]
                  }
    if parameters['main'][0]:
        loc_param = parameters['main'][1]
        # index folder - bike of walking
        INDEX_FOLDER = ['bike_index', 'walking_index']
        # what is the method to standardize the data (zscore or rank)
        METHOD = ['rank', 'zscore']
        # tuples of columns, so the code loops over each tuple column
        TUPLES = [['LongBeach_streetlight', 'LongBeach_strava'], ['SanLuisObispo_streetlight', 'SanLuisObispo_strava'],
                  ['SantaBarbara_streetlight', 'SantaBarbara_strava'], ['SantaMaria_streetlight', 'SantaMaria_strava']]
        # Month to drop in the analysis part
        MONTHS_TO_DROP = ['2018_12']
        # data about the number of victims killed & injured.
        city_crashes = {'walking': {'LongBeach': 383, 'SanLuisObispo': 25, 'SantaBarbara': 62, 'SantaMaria': 22},
                        'bike': {'LongBeach': 218, 'SanLuisObispo': 40, 'SantaBarbara': 81, 'SantaMaria': 14}}

        # END PARAMETER SECTION #

        for index_folder in INDEX_FOLDER:
            print(index_folder)
            if loc_param['div_to_count']:
                # Get the pedestrian count for each place for the months between 2018 and 2021.
                # This data is stored as a dictionary of places and HTML elements
                print('div_to_count')
                for my_html in my_dic.items():
                    div_to_count(my_html)

            folder_data = os.path.join(index_folder, 'streetlight', 'by_month')
            if loc_param['unzip']:
                print('unzip')
                unzip(path_to_years=folder_data)

            res_loc = os.path.join(folder_data, 'data.csv')
            if loc_param['prepare_street_light_data']:
                print('prepare_street_light_data')
                sl_user = 'ped' if INDEX_FOLDER == 'walking_index' else 'bike'
                res = prepare_street_light_data(path_to_years=folder_data, sl_user=sl_user)
                res.to_csv(res_loc)

            com_file = os.path.join(index_folder, 'comparison.csv')
            if loc_param['update_file_street_light']:
                print('update_file_street_light')
                update_file_street_light(res_loc).to_csv(com_file)

            strava_folder = os.path.join(index_folder, 'strava')
            final = os.path.join(index_folder, 'final.csv')
            if loc_param['merge_strava_sl']:
                print('merge_strava_sl')
                merge_strava_sl(folder_strava=strava_folder, file_sl=pd.read_csv(com_file)).to_csv(final)
            if loc_param['draw_results']:
                print('draw_results')
                df = pd.read_csv(final)
                df = df[~df['date'].isin(MONTHS_TO_DROP)]
                draw_results(df, TUPLES, index_folder)
            for method in METHOD:
                print(method)
                mu_rank = os.path.join(index_folder, method + '.csv')
                if parameters['draw_results_method']:
                    print('draw_results_method')
                    df = pd.read_csv(final)
                    df = df[~df['date'].isin(MONTHS_TO_DROP)]
                    draw_results_ranking(df, TUPLES, method, index_folder).to_csv(mu_rank)

                classes = os.path.join(index_folder, 'classes_' + method + '.csv')
                if parameters['calculate_avg_std']:
                    print('calculate_avg_std')
                    df = pd.read_csv(mu_rank)
                    city_crashes_method = city_crashes['bike'] if index_folder == 'bike_index' else city_crashes[
                        'walking']
                    calculate_avg_std_index(df, TUPLES, city_crashes_method).to_csv(classes)

            if loc_param['calculate_count_ml']:
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
    if parameters['validation'][0]:
        print('validation')
        loc_param = parameters['validation'][1]
        my_validation = Validation(folder_data='validation', raw_data_path='export.csv')
        if loc_param['draw_count_time_two_streets']:
            print('draw_count_time_two_streets')
            my_validation.draw_count_time_two_streets()
