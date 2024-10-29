import geopandas as gpd
import pandas as pd
import os

blocks = gpd.read_file('output/intermediate/superblocks_mannheim/results_block_all.shp')
education = gpd.read_file('output/intermediate/poi_isochrones/Education_id.geojson')
recreation = gpd.read_file('output/intermediate/poi_isochrones/Recreation_id.geojson')
health = gpd.read_file('output/intermediate/poi_isochrones/Health_id.geojson')
commercial = gpd.read_file('output/intermediate/poi_isochrones/Commercial_id.geojson')
food = gpd.read_file('output/intermediate/poi_isochrones/Food_id.geojson')
iso_education = gpd.read_file('output/intermediate/poi_isochrones_merged/Education_merged.geojson')
iso_recreation = gpd.read_file('output/intermediate/poi_isochrones_merged/Recreation_merged.geojson')
iso_health = gpd.read_file('output/intermediate/poi_isochrones_merged/Health_merged.geojson')
iso_commercial = gpd.read_file('output/intermediate/poi_isochrones_merged/Commercial_merged.geojson')
iso_food = gpd.read_file('output/intermediate/poi_isochrones_merged/Food_merged.geojson')

iso_education['poi_id'] = iso_education['poi_id'].astype(str)
education['poi_id'] = education['poi_id'].astype(str)
iso_recreation['poi_id'] = iso_recreation['poi_id'].astype(str)
recreation['poi_id'] = recreation['poi_id'].astype(str)
iso_health['poi_id'] = iso_health['poi_id'].astype(str)
health['poi_id'] = health['poi_id'].astype(str)
iso_commercial['poi_id'] = iso_commercial['poi_id'].astype(str)
commercial['poi_id'] = commercial['poi_id'].astype(str)
iso_food['poi_id'] = iso_food['poi_id'].astype(str)
food['poi_id'] = food['poi_id'].astype(str)

columns_to_merge = ['shop', 'amenity', 'leisure', 'tourism']
existing_columns_education = [col for col in columns_to_merge if col in education.columns]
existing_columns_recreation = [col for col in columns_to_merge if col in recreation.columns]
existing_columns_health = [col for col in columns_to_merge if col in health.columns]
existing_columns_commercial = [col for col in columns_to_merge if col in commercial.columns]
existing_columns_food = [col for col in columns_to_merge if col in food.columns]

iso_education = iso_education.merge(education[['poi_id'] + existing_columns_education], on='poi_id', how='left')
iso_recreation = iso_recreation.merge(recreation[['poi_id'] + existing_columns_recreation], on='poi_id', how='left')
iso_health = iso_health.merge(health[['poi_id'] + existing_columns_health], on='poi_id', how='left')
iso_commercial = iso_commercial.merge(commercial[['poi_id'] + existing_columns_commercial], on='poi_id', how='left')
iso_food = iso_food.merge(food[['poi_id'] + existing_columns_food], on='poi_id', how='left')

iso_education.to_file('output/intermediate/Education_merged_with_columns.geojson', driver='GeoJSON')
iso_recreation.to_file('output/intermediate/Recreation_merged_with_columns.geojson', driver='GeoJSON')
iso_health.to_file('output/intermediate/Health_merged_with_columns.geojson', driver='GeoJSON')
iso_commercial.to_file('output/intermediate/Commercial_merged_with_columns.geojson', driver='GeoJSON')
iso_food.to_file('output/intermediate/Food_merged_with_columns.geojson', driver='GeoJSON')
print("Merged GeoDataFrames saved successfully.")

iso_education['time_range'] = pd.to_numeric(iso_education['time_range'])
iso_recreation['time_range'] = pd.to_numeric(iso_recreation['time_range'])
iso_health['time_range'] = pd.to_numeric(iso_health['time_range'])
iso_commercial['time_range'] = pd.to_numeric(iso_commercial['time_range'])
iso_food['time_range'] = pd.to_numeric(iso_food['time_range'])

blocks = blocks.to_crs(epsg=25832)
education = education.to_crs(epsg=25832)
recreation = recreation.to_crs(epsg=25832)
health = health.to_crs(epsg=25832)
commercial = commercial.to_crs(epsg=25832)
food = food.to_crs(epsg=25832)
iso_education = iso_education.to_crs(epsg=25832)
iso_recreation = iso_recreation.to_crs(epsg=25832)
iso_health = iso_health.to_crs(epsg=25832)
iso_commercial = iso_commercial.to_crs(epsg=25832)
iso_food = iso_food.to_crs(epsg=25832)

def count_unique_values_as_columns(iso_data, block_data, columns):
    blocks_within_iso = blocks[blocks.geometry.apply(lambda x: any(x.within(iso) for iso in iso_data.geometry))].copy()
    counts_df = pd.DataFrame(index=blocks_within_iso.index)
    for col in columns:
        if col in iso_data.columns:
            unique_values = iso_data[col].unique()
            for value in unique_values:
                if pd.notna(value):
                    counts_df[value] = 0
                    for idx, block in blocks_within_iso.iterrows():
                        intersecting_iso = iso_data[iso_data.geometry.intersects(block.geometry)]
                        count = (intersecting_iso[col] == value).sum()
                        counts_df.at[idx, value] += count
    result_df = pd.concat([blocks_within_iso, counts_df], axis=1)
    return result_df


blocks = blocks
iso_data_list = [
    (iso_health, 'health_blocks.geojson'),
    (iso_education, 'education_blocks.geojson'),
    (iso_recreation, 'recreation_blocks.geojson'),
    (iso_commercial, 'commercial_blocks.geojson'),
    (iso_food, 'food_blocks.geojson'),
]

# Specify the columns you want to count
columns_to_count = ['tourism', 'leisure', 'amenity', 'shop']

# Loop through each iso_data and process it
for iso_data, output_filename in iso_data_list:
    blocks_with_counts = count_unique_values_as_columns(iso_data, blocks, columns_to_count)
    output_path = f'output/intermediate/{output_filename}'
    blocks_with_counts.to_file(output_path, driver='GeoJSON')

