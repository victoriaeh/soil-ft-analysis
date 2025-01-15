# transform input data: create one csv file for each site containing all
# variables for that site - resulting in 16 new files

import sys
print(sys.executable)


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import csv

directory = "/input_data"
csv_list = [
    'air_avg.csv',
    'air_obs.csv',
    'soil_obs_00.csv',
    'soil_obs_02.csv',
    'soil_obs_04.csv',
    'soil_obs_08.csv',
    'soil_obs_20.csv',
    'soil_obs_40.csv',
    'soil_avg_00.csv',
    'soil_avg_02.csv',
    'soil_avg_04.csv',
    'soil_avg_08.csv',
    'soil_avg_20.csv',
    'soil_avg_40.csv']
# csv_dict = {
#     'air_avg': 'air_avg.csv',
#     'air_obs': 'air_obs.csv',
#     'soil_obs_00': 'soil_obs_00.csv',
#     'soil_obs_02': 'soil_obs_02.csv',
#     'soil_obs_04': 'soil_obs_04.csv',
#     'soil_obs_08': 'soil_obs_08.csv',
#     'soil_obs_20': 'soil_obs_20.csv',
#     'soil_obs_40': 'soil_obs_40.csv',
#     'soil_avg_00': 'soil_avg_00.csv',
#     'soil_avg_02': 'soil_avg_02.csv',
#     'soil_avg_04': 'soil_avg_04.csv',
#     'soil_avg_08': 'soil_avg_08.csv',
#     'soil_avg_20': 'soil_avg_20.csv',
#     'soil_avg_40': 'soil_avg_40.csv'}


for csv_file in csv_list:
    filepath = os.path.join(directory, csv_list)
    df_name = os.path.splitext(csv_file)[0] # basename of csv file
    dataframe = pd.read_csv(filepath, comment='#')
    globals()[df_name] = dataframe

    print(f'{df_name} dataframe created successfully')

