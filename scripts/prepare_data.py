import pandas as pd
import geopandas as gpd

# --------------------------------------------------
# 1. File paths
# --------------------------------------------------

taxi_file = "data/yellow_tripdata_2026-01.parquet"
zone_file = "data/taxi_zones/taxi_zones/taxi_zones.shp"
output_file = "data/cleaned_taxi_data.parquet"

# --------------------------------------------------
# 2. Load Taxi Zone data
# --------------------------------------------------

print("Loading taxi zones...")

zones = gpd.read_file(zone_file)

# Calculate centroid in the original projected CRS
zones["centroid"] = zones.geometry.centroid

# Convert centroid to WGS84
centroids = zones.set_geometry("centroid").to_crs(epsg=4326)

# Extract coordinates
zones["longitude"] = centroids.geometry.x
zones["latitude"] = centroids.geometry.y

# Keep only the fields we need
zone_mapping = zones[
    ["LocationID", "longitude", "latitude"]
].copy()

print("Taxi zones loaded:", len(zone_mapping))

# --------------------------------------------------
# 3. Load taxi dataset
# --------------------------------------------------

print("\nLoading taxi dataset...")

df = pd.read_parquet(taxi_file)

print("Original records:", len(df))

# --------------------------------------------------
# 4. Take first 500,000 records
# --------------------------------------------------

df = df.head(500_000).copy()

print("Records selected:", len(df))

# --------------------------------------------------
# 5. Rename important columns
# --------------------------------------------------

df = df.rename(columns={
    "tpep_pickup_datetime": "pickup_time",
    "tpep_dropoff_datetime": "dropoff_time",
    "PULocationID": "pickup_location_id",
    "DOLocationID": "dropoff_location_id"
})

# --------------------------------------------------
# 6. Convert Location IDs to integers
# --------------------------------------------------

df["pickup_location_id"] = pd.to_numeric(
    df["pickup_location_id"],
    errors="coerce"
)

df["dropoff_location_id"] = pd.to_numeric(
    df["dropoff_location_id"],
    errors="coerce"
)

# --------------------------------------------------
# 7. Map pickup coordinates
# --------------------------------------------------

pickup_mapping = zone_mapping.rename(columns={
    "LocationID": "pickup_location_id",
    "longitude": "pickup_longitude",
    "latitude": "pickup_latitude"
})

df = df.merge(
    pickup_mapping,
    on="pickup_location_id",
    how="left"
)

# --------------------------------------------------
# 8. Map dropoff coordinates
# --------------------------------------------------

dropoff_mapping = zone_mapping.rename(columns={
    "LocationID": "dropoff_location_id",
    "longitude": "dropoff_longitude",
    "latitude": "dropoff_latitude"
})

df = df.merge(
    dropoff_mapping,
    on="dropoff_location_id",
    how="left"
)

# --------------------------------------------------
# 9. Remove records without coordinates
# --------------------------------------------------

before = len(df)

df = df.dropna(
    subset=[
        "pickup_longitude",
        "pickup_latitude",
        "dropoff_longitude",
        "dropoff_latitude"
    ]
)

print("\nRecords removed because of missing coordinates:",
      before - len(df))

print("Clean records:", len(df))

# --------------------------------------------------
# 10. Create taxi ID
# --------------------------------------------------

df.insert(
    0,
    "taxi_id",
    range(1, len(df) + 1)
)

# --------------------------------------------------
# 11. Select final columns
# --------------------------------------------------

df = df[
    [
        "taxi_id",
        "pickup_time",
        "dropoff_time",
        "pickup_location_id",
        "pickup_longitude",
        "pickup_latitude",
        "dropoff_location_id",
        "dropoff_longitude",
        "dropoff_latitude",
        "passenger_count",
        "trip_distance",
        "fare_amount"
    ]
]

# --------------------------------------------------
# 12. Save cleaned dataset
# --------------------------------------------------

df.to_parquet(
    output_file,
    index=False
)

print("\nCleaned dataset saved successfully!")

print("Output file:", output_file)
print("Final records:", len(df))
print("Final columns:", len(df.columns))