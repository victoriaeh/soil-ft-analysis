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

#########################
#
# Perform PCA on the data
#
#########################

# select observational or daily average dictionary
working_dict = avg_dict

# center and scale data for PCA
scaled_data = StandardScaler().fit_transform(working_dict)
# create PCA object
pca = PCA()
# calculate loading scores and variation for each principle component
pca.fit(scaled_data)
# generate coords for PCA graph based on loading scores and scaled data
pca_data = pca.transform(scaled_data)

#########################
#
# Draw Scree plots and PCA plots
#
#########################

# generate scree plot
per_var = np.round(pca.explained_variance_ratio_* 100, decimals=1)
labels = ['PC' + str(x) for x in range(1, len(per_var)+1)]

plt.bar(x=range(1, len(per_var)+1), height=per_var, tick_label=labels)
plt.ylabel('Percentage fo Explained Variance')
plt.xlabel('Principle Component')
plt.title('Scree Plot')
plt.show()

# # draw PCA plot where rows have sample labels and columns have PC labels
# pca_df = pd.DataFrame(pca_data, index=[], columns=labels)

# plt.scatter(pca_df.PC1, pca_df.PC2)
# plt.title('My PCA Graph')
# plt.xlabel('PC1 - {0}%'.format(per_var[0]))
# plt.ylabel('PC2 - {0}%'.format(per_var[0]))
# # add sample names to graph
# for sample in pca_df.index:
#     plt.annotate(sample, (pca_df.PC1.loc[sample], pca_df.PC2.loc[sample]))
# plt.show()

#########################
#
# Determine which variables had the biggest influence on PCA
#
#########################

# # examine loading scores
# loading_scores = pd.Series(pca.components_[0], index=)
# sorted_loading_scores = loading_scores.abs().sort_values(ascending=False)

# top_5_variables = sorted_loading_scores[0:5].index.values

# print(loading_scores[top_5_variables])