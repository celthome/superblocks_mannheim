import geopandas as gpd

def check_criteria_and_save(input_path, output_path, criteria_func):
    blocks = gpd.read_file(input_path)
    blocks['meets_criteria'] = blocks.apply(criteria_func, axis=1)
    filtered_blocks = blocks[blocks['meets_criteria']]
    filtered_blocks.to_file(output_path, driver='GeoJSON')
    print(f"Criteria checked and saved for blocks that meet the criteria in {output_path}.")

def check_education_criteria(block):
    has_primary_or_middle = block['kindergarten'] >= 1 or block['school'] >= 1
    has_secondary = block['college'] >= 1 or block['university'] >= 1
    return has_primary_or_middle and has_secondary

def check_recreation_criteria(block):
    has_restaurant = block['restaurant'] >= 1
    has_alternative_facility = (
        block['cinema'] >= 1 or
        block['library'] >= 1 or
        block['fitness_centre'] >= 1 or
        block['sports_centre'] >= 1 or
        block['community_centre'] >= 1 or
        block['fitness_station'] >= 1 or
        block['concert_hall'] >= 1
    )
    has_park = block['playground'] >= 1
    return has_restaurant and has_alternative_facility and has_park

def check_health_criteria(block):
    has_doctor_or_hospital = block['doctors'] >= 1 or block['hospital'] >= 1 or block['dentist'] >= 1
    has_pharmacy = block['pharmacy'] >= 1
    return has_doctor_or_hospital and has_pharmacy

def check_commercial_criteria(block):
    has_store = block['department_store'] >= 1 or block['convenience'] >= 1 or block['general'] >= 1 or block['kiosk'] >= 1
    has_bank = block['bank'] >= 1
    return has_store and has_bank

def check_food_criteria(block):
    has_grocery_store = block['supermarket'] >= 1 or block['fast_food'] >= 1
    specialty_stores_count = block['greengrocer'] + block['butcher']
    has_specialty_food_stores = specialty_stores_count >= 3
    return has_grocery_store or has_specialty_food_stores

datasets = [
    ('output/intermediate/education_blocks.geojson', 'output/intermediate/checked_education_blocks.geojson', check_education_criteria),
    ('output/intermediate/recreation_blocks.geojson', 'output/intermediate/checked_recreation_blocks.geojson', check_recreation_criteria),
    ('output/intermediate/health_blocks.geojson', 'output/intermediate/checked_health_blocks.geojson', check_health_criteria),
    ('output/intermediate/commercial_blocks.geojson', 'output/intermediate/checked_commercial_blocks.geojson', check_commercial_criteria),
    ('output/intermediate/food_blocks.geojson', 'output/intermediate/checked_food_blocks.geojson', check_food_criteria)
]

for input_path, output_path, criteria_func in datasets:
    check_criteria_and_save(input_path, output_path, criteria_func)


edu_blocks = gpd.read_file('output/intermediate/checked_education_blocks.geojson')
rec_blocks = gpd.read_file('output/intermediate/checked_recreation_blocks.geojson')
health_blocks = gpd.read_file('output/intermediate/checked_health_blocks.geojson')
commercial_blocks = gpd.read_file('output/intermediate/checked_commercial_blocks.geojson')
food_blocks = gpd.read_file('output/intermediate/checked_food_blocks.geojson')

common_blocks = (
    edu_blocks.merge(rec_blocks, on='inter_id', suffixes=('_edu', '_rec'))
    .merge(health_blocks, on='inter_id', suffixes=('', '_health'))
    .merge(commercial_blocks, on='inter_id', suffixes=('', '_commercial'))
    .merge(food_blocks, on='inter_id', suffixes=('', '_food'))
)

geometry_cols = [col for col in common_blocks.columns if col.startswith('geometry')]
print("Geometry columns found:", geometry_cols)

if geometry_cols:
    common_blocks = common_blocks.drop(columns=geometry_cols[1:])
    common_blocks = gpd.GeoDataFrame(common_blocks, geometry=geometry_cols[0])
else:
    raise ValueError("No geometry column found after merging.")

common_blocks.to_file('output/common_blocks.geojson', driver='GeoJSON')

print("Common blocks across all categories saved.")
