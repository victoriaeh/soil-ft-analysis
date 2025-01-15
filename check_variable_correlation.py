# check if variables intended for multiple regression analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('site_data/aniak.csv', index_col=0)

correlation_matrix = data.corr()

fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.matshow(correlation_matrix, cmap='coolwarm', vmin=-1, vmax=1)
fig.colorbar(cax)
ticks = np.arange(0, len(data.columns), 1)
ax.set_xticks(ticks)
plt.xticks(rotation=90)
ax.set_yticks(ticks)
ax.set_xticklabels(data.columns)
ax.set_yticklabels(data.columns)
plt.subplots_adjust(top=0.7)
plt.show()