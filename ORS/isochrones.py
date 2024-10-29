import os
import time
import json
import geopandas as gpd
from openrouteservice import Client, exceptions


def calculate_isochrones_with_retry(client, coordinate, profile, range_type, range_seconds):
    retries = 3
    for attempt in range(retries):
        try:
            isochrones = client.isochrones(
                locations=[coordinate],
                profile=profile,
                range_type=range_type,
                range=range_seconds
            )
            return isochrones
        except exceptions.ApiError as e:
            if "rate limit exceeded" in str(e).lower():
                print(f"Rate limit exceeded. Retrying in 10 seconds...")
                time.sleep(10)
            elif "unable to build an isochrone map" in str(e).lower():
                print(f"Unable to build an isochrone map for coordinate {coordinate}. Skipping...")
                return None
            else:
                raise e
    return None


def process_geojson_files(client, input_folder, profile, range_type, range_times, output_folder):
    geojson_files = [f for f in os.listdir(input_folder) if f.endswith('.geojson')]
    for geojson_file in geojson_files:
        input_path = os.path.join(input_folder, geojson_file)
        pois = gpd.read_file(input_path)
        if pois.crs != "EPSG:4326":
            pois = pois.to_crs(epsg=4326)
        pois['poi_id'] = range(1, len(pois) + 1)
        output_geojson_with_id = os.path.join(output_folder, f'{os.path.splitext(geojson_file)[0]}_id.geojson')
        pois.to_file(output_geojson_with_id, driver='GeoJSON')
        print(f"Saved {output_geojson_with_id} with POI IDs.")
        for idx, row in pois.iterrows():
            lon, lat = row['geometry'].x, row['geometry'].y
            coordinate = (lon, lat)
            for time_in_seconds in range_times:
                isochrones = calculate_isochrones_with_retry(
                    client, coordinate, profile, range_type, [time_in_seconds])
                if isochrones is None:
                    continue
                for feature in isochrones['features']:
                    feature['properties']['poi_id'] = row['poi_id']
                time_in_minutes = time_in_seconds // 60
                name_without_extension = os.path.splitext(geojson_file)[0]
                output_filename = os.path.join(
                    output_folder, f'{name_without_extension}_{row["poi_id"]}_{time_in_minutes}.geojson')
                with open(output_filename, 'w') as output_file:
                    json.dump(isochrones, output_file)
                print(f"Isochrones saved for POI {row['poi_id']} ({time_in_minutes} minutes) to {output_filename}")
                time.sleep(1)

api_key = "API-KEY"  # Replace with your actual API key
client = Client(key=api_key)
profile = 'foot-walking'
range_type = 'time'
range_seconds = [300] # 5 minutes

input_folder = 'output/intermediate/poi'
output_folder = 'output/intermediate/poi_isochrones'
os.makedirs(output_folder, exist_ok=True)
process_geojson_files(
    client, input_folder, profile, range_type, range_seconds, output_folder)

print(f"Isochrone calculation completed for all files.")
