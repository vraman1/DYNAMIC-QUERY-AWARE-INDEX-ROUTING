import geopandas as gpd

file_path = "data/taxi_zones/taxi_zones/taxi_zones.shp"

zones = gpd.read_file(file_path)

print("\nTaxi zone dataset loaded successfully!")

print("Number of zones:", len(zones))
print("Number of columns:", len(zones.columns))

print("\nColumns:")
for column in zones.columns:
    print("-", column)

print("\nCoordinate Reference System:")
print(zones.crs)

print("\nFirst 5 records:")
print(zones.head())