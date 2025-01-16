# check if variables intended for multiple regression analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def get_csv_files(directory):
    """Create a dictionary of CSV files as dataframes contained in a directory"""
    csv_files = {}
    for file in os.listdir(directory):
        if file.endswith('.csv'):
            filepath = os.path.join(directory, file)
            site_name = os.path.splitext(file)[0]
            csv_files[site_name] = pd.read_csv(filepath, index_col=0)
    return csv_files

def get_correlation_matrix(data, dir_path='./'):
    """Create a correlation matrix for each dataframe in data
    Args: 
        1. Data: dictionary with dataframes of csv files
        2. Dir_path: directory path to save the figures
    Steps: 
        1. Get the site name from the csv file name
        2. Get the correlation matrix
        3. Create and export figure of matrix using seaborn
        """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    
    for site_name, dataframe in data.items(): 
        correlation_matrix = dataframe.corr()
        fig, ax = plt.subplots(figsize=(7, 4))
        sns.heatmap(correlation_matrix, annot=True, fmt='.2f',
                    cmap=plt.get_cmap('coolwarm'), cbar=False, ax=ax, 
                    vmin = -1, vmax=1)
        ax.xaxis.tick_top()
        ax.set_title(f'{site_name.title()} correlation matrix')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='left')
        ax.set_yticklabels(ax.get_yticklabels(), rotation='horizontal')
        plt.savefig(f'{dir_path}/corr_matrix_{site_name}.png', bbox_inches='tight', 
                    pad_inches=0.1, dpi=300)

directory = 'site_data'
data = get_csv_files(directory)

fig_dir = 'corr_matrix_figures'
get_correlation_matrix(data, fig_dir)




# # import csv
# data = pd.read_csv('site_data/aniak.csv', index_col=0)
# # site_name = 
# # create correlation matrix
# correlation_matrix = data.corr()
# # plot and export matrix
# fig, ax = plt.subplots(figsize=(7, 4))
# sns.heatmap(correlation_matrix, annot=True, fmt='.2f',
#             cmap=plt.get_cmap('coolwarm'), cbar=False, ax=ax)
# ax.xaxis.tick_top()
# ax.set_title('Aniak correlation matrix')
# ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='left')
# ax.set_yticklabels(ax.get_yticklabels(), rotation='horizontal')
# plt.savefig('correlation_matrix.png', bbox_inches='tight', pad_inches=0.1, 
#             dpi=300)