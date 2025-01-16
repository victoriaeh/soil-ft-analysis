# check if variables intended for multiple regression analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def get_csv_files(directory):
    """
    Create a dictionary of CSV files as dataframes contained in a directory
    """
    csv_files = {}
    for file in os.listdir(directory):
        if file.endswith('.csv'):
            filepath = os.path.join(directory, file)
            site_name = os.path.splitext(file)[0]
            csv_files[site_name] = pd.read_csv(filepath, index_col=0)
    return csv_files

def subset_dataframes(subset, data):
    """
    Subset the dataframes for either average daily or am observed data
    """
    data_subset = {}
    for site_name, dataframe in data.items():
        selected_columns = [col for col in dataframe.columns if subset in col]
        data_subset[site_name] = dataframe[selected_columns]
    return data_subset


def get_correlation_matrix(data_subset, observation_type, subset, dir_path='./'):
    """
    Create a correlation matrix for each dataframe in the dictionary
    Args: 
        1. Data_subset: dictionary with subsetted dataframes of csv files
        2. Observation_type: either average or observed
        4. Susbet: either avg or obs - determined from argument used in
            subset_dataframes 
        2. Dir_path: directory path to save the figures
    Steps: 
        1. Get the site name from the csv file name
        2. Get the correlation matrix
        3. Create and export figure of matrix using seaborn
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    
    for site_name, dataframe in data_subset.items(): 
        correlation_matrix = dataframe.corr()
        fig, ax = plt.subplots(figsize=(4, 3))
        sns.heatmap(correlation_matrix, annot=True, fmt='.2f',
                    cmap=plt.get_cmap('coolwarm'), cbar=False, ax=ax, 
                    vmin = -1, vmax=1)
        ax.xaxis.tick_top()
        ax.set_title(
            f'{site_name.title()} {observation_type} correlation matrix')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='left')
        ax.set_yticklabels(ax.get_yticklabels(), rotation='horizontal')
        plt.savefig(f'{dir_path}/corr_matrix_{subset}_{site_name}.png', 
                    bbox_inches='tight', pad_inches=0.1, dpi=300)
        plt.close(fig)

# store the csvs as dataframes in a directory
directory = 'site_data'
data = get_csv_files(directory)

# subset the *_avg columns into a dictionary 
avg_subset = 'avg'
observation_type = 'average'
avg_df = subset_dataframes(avg_subset, data)

# subset the *_obs columns into a dictionary
obs_subset = 'obs'
observation_type = 'observed'
obs_df= subset_dataframes(obs_subset, data)

# process avg_df for correlation matrix and export results
observation_type = 'average'
fig_dir = 'corr_matrix_figures/avg'
get_correlation_matrix(avg_df, observation_type, avg_subset, fig_dir)

# process obs_df for correlation matrix and export results
observation_type = 'observed'
fig_dir = 'corr_matrix_figures/obs'
get_correlation_matrix(obs_df, observation_type, obs_subset, fig_dir)

