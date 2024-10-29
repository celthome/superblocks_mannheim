import requests
import json
import os

overpass_url = "http://overpass-api.de/api/interpreter"
bbox = "49.479613,8.452864,49.496619,8.481789"
save_directory = "output/intermediate/poi"
os.makedirs(save_directory, exist_ok=True)

queries = {
    "Food": """
    [out:json][timeout:25];
    (
      node["shop"="supermarket"]({bbox});
      node["shop"="greengrocer"]({bbox});
      node["shop"="butcher"]({bbox});
    );
    out body;
    >;
    out skel qt;
    """,
    "Commercial": """
    [out:json][timeout:25];
    (
      node["shop"="department_store"]({bbox});
      node["shop"="convenience"]({bbox});
      node["shop"="general"]({bbox});
      node["amenity"="bank"]({bbox});
      node["amenity"="post_office"]({bbox});
      node["shop"="mall"]({bbox});
    );
    out body;
    >;
    out skel qt;
    """,
    "Health": """
    [out:json][timeout:25];
    (
      node["amenity"="doctors"]({bbox});
      node["amenity"="pharmacy"]({bbox});
      node["amenity"="hospital"]({bbox});
      node["amenity"="dentist"]({bbox});
    );
    out body;
    >;
    out skel qt;
    """,
    "Recreation": """
    [out:json][timeout:25];
    (
      node["amenity"="restaurant"]({bbox});
      node["amenity"="cinema"]({bbox});
      node["amenity"="library"]({bbox});
      node["amenity"="archive"]({bbox});
      node["leisure"="fitness_centre"]({bbox});
      node["amenity"="community_centre"]({bbox});
      node["leisure"="park"]({bbox});
      node["amenity"="cafe"]({bbox});
      node["amenity"="theatre"]({bbox});
      node["amenity"="opera"]({bbox});
      node["amenity"="concert_hall"]({bbox});
      node["leisure"="swimming_pool"]({bbox});
      node["tourism"="museum"]({bbox});
      node["tourism"="art_gallery"]({bbox});
      node["leisure"="playground"]({bbox});
      node["leisure"="golf_course"]({bbox});
      node["leisure"="skatepark"]({bbox});
      node["leisure"="sports_centre"]({bbox});
      node["tourism"="zoo"]({bbox});
      node["tourism"="amusement_park"]({bbox});
      node["leisure"="nature_reserve"]({bbox});
      node["tourism"="camp_site"]({bbox});
      node["leisure"="dog_park"]({bbox});
      node["leisure"="picnic_table"]({bbox});
      node["leisure"="fitness_station"]({bbox});
      node["leisure"="water_park"]({bbox});
      node["amenity"="fast_food"]({bbox});
      node["amenity"="pub"]({bbox});
      node["amenity"="bar"]({bbox});
    );
    out body;
    >;
    out skel qt;
    """
    ,
    "Education": """
    [out:json][timeout:25];
    (
      node["amenity"="school"]({bbox});
      node["amenity"="kindergarten"]({bbox});
      node["amenity"="university"]({bbox});
      node["amenity"="college"]({bbox});
    );
    out body;
    >;
    out skel qt;
    """
}

def execute_query_and_save_geojson(query, category):
    response = requests.post(overpass_url, data={'data': query.format(bbox=bbox)})
    data = response.json()
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }
    for element in data['elements']:
        if 'lat' in element and 'lon' in element:
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [element['lon'], element['lat']]
                },
                "properties": element.get("tags", {})
            }
            geojson["features"].append(feature)
        elif 'nodes' in element:
            coordinates = []
            for node in element['nodes']:
                node_data = next((item for item in data['elements'] if item['id'] == node), None)
                if node_data and 'lat' in node_data and 'lon' in node_data:
                    coordinates.append([node_data['lon'], node_data['lat']])
            if coordinates:
                feature = {
                    "type": "Feature",
                    "geometry": {
                        "type": "LineString",
                        "coordinates": coordinates
                    },
                    "properties": element.get("tags", {})
                }
                geojson["features"].append(feature)
    filepath = os.path.join(save_directory, f"{category}.geojson")
    with open(filepath, 'w') as file:
        json.dump(geojson, file, indent=2)
for category, query in queries.items():
    execute_query_and_save_geojson(query, category)