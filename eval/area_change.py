import geopandas as gpd
import os


def shp_into_geojson(shp, output):
    gdf = gpd.read_file(shp)
    gdf.to_file(output, driver='GeoJSON')
    print(f"Saved {output} as GeoJSON.")
    return gdf

shapefile_dir = 'output/intermediate/superblocks_mannheim'
for file in os.listdir(shapefile_dir):
    if file.endswith('.shp'):
        shp_path = os.path.join(shapefile_dir, file)
        geojson_path = shp_path.replace('.shp', '.geojson')
        shp_into_geojson(shp_path, geojson_path)

shapefile_dir = 'output/nm/'
for file in os.listdir(shapefile_dir):
    if file.endswith('.shp'):
        shp_path = os.path.join(shapefile_dir, file)
        geojson_path = shp_path.replace('.shp', '.geojson')
        shp_into_geojson(shp_path, geojson_path)

# area in block absolute and relative
def crop_to_superblock(nm_path, blocks_path, output_path):
    contour_gdf = gpd.read_file(nm_path)
    blocks_gdf = gpd.read_file(blocks_path)
    if contour_gdf.crs != blocks_gdf.crs:
        contour_gdf = contour_gdf.to_crs(blocks_gdf.crs)
    cropped_gdf = gpd.overlay(contour_gdf, blocks_gdf, how='intersection')
    cropped_gdf.to_file(output_path, driver='GeoJSON')
    print(f"NM cropped to superblocks and saved to {output_path}")

blocks_path = 'output/common_blocks.geojson'
nm_dir = 'output/nm/'

for file in os.listdir(nm_dir):
    if file.endswith('.geojson'):
        nm_path = os.path.join(nm_dir, file)
        output_path = nm_path.replace('.geojson', '_cropped.geojson')
        crop_to_superblock(nm_path, blocks_path, output_path)

def calculate_area_and_update_geojson(input_path):
    gdf = gpd.read_file(input_path)
    if gdf.crs != 'EPSG:32632':
        gdf = gdf.to_crs('EPSG:32632')
    gdf['area_m2'] = gdf.geometry.area
    gdf.to_file(input_path, driver='GeoJSON')
    print(f"Updated {input_path} with new area_m2 column.")

nm_dir = 'output/nm/'

for file in os.listdir(nm_dir):
    if file.endswith('_cropped.geojson'):
        input_path = os.path.join(nm_dir, file)
        calculate_area_and_update_geojson(input_path)



def calculate_change(baseline_path, nm_path, output_csv_path):
    baseline_gdf = gpd.read_file(baseline_path)
    nm_gdf = gpd.read_file(nm_path)

    baseline_area_sum = baseline_gdf.groupby('ISOLABEL')['area_m2'].sum().reset_index()
    nm_area_sum = nm_gdf.groupby('ISOLABEL')['area_m2'].sum().reset_index()

    merged_df = baseline_area_sum.merge(nm_area_sum, on='ISOLABEL', suffixes=('_baseline', '_nm'))
    merged_df['area_difference'] = merged_df['area_m2_nm'] - merged_df['area_m2_baseline']
    merged_df['percentage_change'] = ((merged_df['area_m2_nm'] - merged_df['area_m2_baseline'])/merged_df['area_m2_baseline']) * 100

    merged_df.rename(columns={
        'area_m2_baseline': 'area_original',
        'area_m2_nm': 'area_after_change'
    }, inplace=True)

    merged_df.to_csv(output_csv_path, index=False)
    print(f"Results saved to {output_csv_path}")

baseline_path = 'output/nm/baseline.geojson'
nm_dir = 'output/nm/'
output_dir = 'output/area'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for file in os.listdir(nm_dir):
    if file.endswith('_cropped.geojson') and file != 'baseline_cropped.geojson':
        nm_path = os.path.join(nm_dir, file)
        output_csv_path = os.path.join(output_dir, file.replace('_cropped.geojson', '_area_change.csv'))
        calculate_change(baseline_path, nm_path, output_csv_path)

