import os
import geopandas as gpd
import pandas as pd


def merge_isochrones_per_category(input_folder, output_folder):
    geojson_files = [f for f in os.listdir(input_folder) if f.endswith('.geojson')]
    category_dataframes = {}
    for geojson_file in geojson_files:
        parts = geojson_file.split('_')
        if len(parts) < 3:
            print(f"Skipping '{geojson_file}': not enough parts in filename.")
            continue
        category = parts[0]
        poi_id = parts[1]
        time_range = parts[2].replace('.geojson', '')
        input_path = os.path.join(input_folder, geojson_file)
        gdf = gpd.read_file(input_path)
        gdf['time_range'] = time_range
        gdf['poi_id'] = poi_id
        if category not in category_dataframes:
            category_dataframes[category] = gdf
        else:
            category_dataframes[category] = pd.concat([category_dataframes[category], gdf], ignore_index=True)
    for category, merged_gdf in category_dataframes.items():
        output_file_path = os.path.join(output_folder, f'{category}_merged.geojson')
        merged_gdf.to_file(output_file_path, driver='GeoJSON')
        print(f"Merged GeoJSON for category '{category}' saved as '{output_file_path}'.")


input_folder = 'output/intermediate/poi_isochrones'
output_folder = 'output/intermediate/poi_isochrones_merged'
os.makedirs(output_folder, exist_ok=True)
merge_isochrones_per_category(input_folder, output_folder)
