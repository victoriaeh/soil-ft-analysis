import os
import pandas as pd

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
