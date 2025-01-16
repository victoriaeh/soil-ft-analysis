import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import os
from load_csv_files import get_csv_files, subset_dataframes

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

