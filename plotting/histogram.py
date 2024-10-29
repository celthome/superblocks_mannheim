import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt

# input random 50 points data with joined official and nm data
gdf = gpd.read_file('input/randompoints.geojson')

mean_values = {
    '< 35': 35,
    '35-40': 37.5,
    '40-45': 42.5,
    '45-50': 47.5,
    '50-55': 52.5,
    '55-60': 57.5,
    '60-65': 62.5,
    '65-70': 67.5,
    '70-75': 72.5,
    '75-80': 77.5,
    '> 80': 80
}

gdf['Expected Mean'] = gdf['ISOLABEL'].map(mean_values)
gdf['Deviation'] = gdf['VALUE'] - gdf['Expected Mean']

if gdf['Deviation'].isnull().any():
    print("NaN values found in 'Deviation'. Dropping rows with NaNs.")
    gdf = gdf.dropna(subset=['Deviation'])
hist_data, bin_edges = np.histogram(gdf['Deviation'], bins=30)
bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])

plt.figure(figsize=(10, 6))
plt.bar(bin_centers, hist_data, width=np.diff(bin_edges), color='#82a6ad', edgecolor='black', alpha=0.6, label='Frequency')

plt.title(r'Deviation between official and modelled data ($\Delta_{val}$)', fontsize=16, fontweight='bold')
plt.xlabel(r'$\Delta_{val}$ (dB(A))', fontsize=14)
plt.ylabel('Frequency', fontsize=14)

plt.xlim(-20, 20)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.legend()
plt.tight_layout()
plt.savefig('figures/histogram.png')
plt.show()
