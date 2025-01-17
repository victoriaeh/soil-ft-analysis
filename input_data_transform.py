import pandas as pd
import os

#########################
#
# Transform input data: create one csv file for each site containing all
# variables for that site, drop empty columns
# - results in 16 new csv files named by the associated snotel site
#########################

directory = "input_data"
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

# initialize empty list for dataframes
df_dict = {}

# load csv files as dataframes
for csv_file in csv_list:
    filepath = os.path.join(directory, csv_file)
    df_name = os.path.splitext(csv_file)[0] # basename of csv file
    dataframe = pd.read_csv(filepath, comment='#')
    dataframe['week_start'] = pd.to_datetime(dataframe['week_start'])
    df_dict[df_name] = dataframe

print(f'df_name dictionary created successfully')

# print(df_dict)

# initialize empty dictionary for site specific dataframes
site_dict = {}

# print(df_dict.keys())

# get column names from df_list for naming site specific dataframes
columns = df_dict['air_avg'].columns.difference(['week_start'])

# create one df for each snotel site (organize data in df_list by snotel site
# instead of by variable)
for df_name, df in df_dict.items():
    for column in df.columns:
        if column != 'week_start':
            # create a temporary dataframe with the selected column renaming
            # the temp_df column based on the original df name
            temp_df = df[[column]].rename(columns={column: 
                                                          f"{df_name}"})
            # drop columns with all NaN values
            temp_df = temp_df.dropna(axis=1, how='all')

            # create a dataframe if site_dict does not yet have one for 
            # the selected column
            if column not in site_dict:
                site_dict[column] = temp_df
            else:
                # otherwise append the new data to the existing dataframe
                site_dict[column] = pd.concat([site_dict[column], 
                                              temp_df], axis=1)

# add index column
for column, dataframe in site_dict.items():
    idx=0
    week_number = range(1, len(dataframe) +1)
    dataframe.insert(loc=idx, column='week_number', value=week_number)

print(f'site_dict dictionary created successfully')

# export dataframes in site_dict to csvs in new folder called site_data
def export_df_to_csv(dictionary, dir_path='./'):
    '''Exports dataframes in a dictionary to CSV files.
    Args: 
        dictionary: A dictionary where keys are dataframe names and
        dir_path: The directory to save the CSV files. Defaults to current dir
    '''
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    
    for df_key, df in dictionary.items():
        file_path = f"{dir_path}/{df_key}.csv"
        df.to_csv(file_path, index=False)

print(site_dict.keys())

site_dir = 'site_data'

export_df_to_csv(site_dict, site_dir)