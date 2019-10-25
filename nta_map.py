from shapely.geometry import Polygon, shape
from matplotlib import colors

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import csv
import json
import sys

df = pd.read_csv(sys.argv[1])


with open('geojson/nta_map.geojson', 'r') as f:
    nta_data = json.load(f)

winners = []
for i, row in df.iterrows():
    for j, cand in enumerate(df.columns):
        if row[j] == row[1:].max():
            winners.append(cand)
            break
ntas = list(df['Neighborhood'])
winner_dict = dict(zip(ntas, winners))

for feat in nta_data['features']:
    feat['properties'].update({'winner' : winner_dict[feat['properties']['ntaname']]})

map_file = sys.argv[1].replace('.csv', '_map.geojson')

with open(map_file, 'w') as f:
    json.dump(nta_data, f)

fig, ax = plt.subplots(1, figsize=(10, 6))
ax.axis('off')
ax.set_title('New York City')
ax.annotate('Source: City of New York Board of Elections', xy=(0.1, 0.08),
xycoords='figure fraction', horizontalalignment='left', verticalalignment='top', fontsize=12, color='#000000')

cmap = colors.ListedColormap(['red', 'brown', 'yellow', 'orange', 'purple', 'green', 'gray', 'pink', 'turquoise', 'blue'])   
nta_map = gpd.read_file(map_file)
nta_map.plot(column='winner', ax=ax, cmap=cmap, edgecolor='0.1', legend=True, legend_kwds={'loc': 'upper left'})
fig.savefig(sys.argv[1].replace('.csv', '_map.png'), dpi=300)

#Comment out below to display window
#plt.show()

