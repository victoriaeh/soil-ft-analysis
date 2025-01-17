import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import os
from load_site_data import get_csv_files, subset_dataframes

#########################
#
# Load csv files from site_data into dictionaries of dataframes
# One dictionary for daily averaged snotel data and one dictionary for 
# am observed snotel data
#
#########################

# store the csvs as dataframes in a directory named data
directory = 'site_data'
data = get_csv_files(directory)

# subset the *_avg columns into a dictionary named avg_dict
subset = 'avg'
observation_type = 'average'
# daily averaged snotel data
avg_dict = subset_dataframes(subset, data)

# subset the *_obs columns into a dictionary named obs_dict
subset = 'obs'
observation_type = 'observed'
# am observed snotel data
obs_dict = subset_dataframes(subset, data)

def scale_and_center_dfs(dictionary):
    """
    Scale and center each dataframe in a dictionary using StandardScaler
    """
    scaled_dict = {}

    for site_name, dataframe in dictionary.items():
        # drop rows with NAN values
        dataframe_clean = dataframe.dropna()

        scaler = StandardScaler()
        scaled_array = scaler.fit_transform(dataframe_clean)

        # convert array back to dataframe
        scaled_dataframe = pd.DataFrame(scaled_array, 
                                        columns=dataframe.columns,
                                        index=dataframe_clean.index)
        
        # store scaled dataframe in new dictionary
        scaled_dict[site_name] = scaled_dataframe
    
    return scaled_dict

def apply_pca(scaled_dict, data_type, scree_path, pca_path):
    """
    1. Apply PCA to dataframes in dictionary
    2. Calculate loading scores and varation for each principle component
    3. Generate coords for PCA graph based on loading scores and scaled data
    4. Draw scree plot
    5. Draw PCA plot
    6. Examine loading scores
    """
    # create PCA object
    pca = PCA()
    
    pca_dict = {}

    # create directories for output figures if they don't already exist
    if not os.path.exists(scree_path):
        os.makedirs(scree_path)
    if not os.path.exists(pca_path):
        os.makedirs(pca_path)

    # loop through dataframes in the dictionary for steps 1 through 6
    for site_name, scaled_data in scaled_dict.items():
        # apply PCA
        pca.fit(scaled_data)
        # get PCA coordinates for scaled_data
        pca_data = pca.transform(scaled_data)
        pca_dict[site_name] = pca_data

        # generate scree plot
        per_var = np.round(pca.explained_variance_ratio_* 100, decimals=1)
        labels = ['PCA' + str(x) for x in range(1, len(per_var)+1)]
        
        fig = plt.figure(figsize=(4, 3))
        plt.bar(x=range(1, len(per_var)+1), height=per_var, tick_label=labels)
        plt.ylabel('Percentage of Explained Variance')
        plt.xlabel('Principle Component')
        plt.title(f'{site_name.title()} {data_type.title()} Scree Plot')
        plt.savefig(f'{scree_path}/scree_plot_{site_name}_{data_type}.png', 
                    bbox_inches='tight', pad_inches=0.1, dpi=300)
        plt.close(fig)

        # draw PCA plot
        pca_df = pd.DataFrame(pca_data, index=scaled_data.index, 
                              columns=labels)
        fig = plt.figure(figsize=(4, 3))
        plt.scatter(pca_df.PCA1, pca_df.PCA2)
        plt.title(f'{site_name.title()} {data_type.title()} PCA Graph')
        plt.xlabel(f'PC1: {per_var[0]}%')
        plt.ylabel(f'PC2: {per_var[1]}%')
        plt.savefig(f'{pca_path}/pca_graph_{site_name}_{data_type}.png', 
                    bbox_inches='tight', pad_inches=0.1, dpi=300)
        plt.close(fig)

        # # examine loading scores
        # loading_scores = pd.Series(pca.components_[0], index=)
        # sorted_loading_scores = loading_scores.abs().sort_values(ascending=
        #                                                          False)
        # top_5_variables = sorted_loading_scores[0:5].index.values
        # # export top_5_variables


# process PCA for daily average dataframes
scaled_dict = scale_and_center_dfs(avg_dict)
data_type = 'average'
# define output figure paths
scree_path = 'figures/average/scree_plot'
pca_path = 'figures/average/pca_plot'
apply_pca(scaled_dict, data_type, scree_path, pca_path)

# process PCA for am observed dataframes
scaled_dict = scale_and_center_dfs(obs_dict)
data_type = 'observed'
# define output figure paths
scree_path = 'figures/observed/scree_plot'
pca_path = 'figures/observed/pca_plot'
apply_pca(scaled_dict, data_type, scree_path, pca_path)