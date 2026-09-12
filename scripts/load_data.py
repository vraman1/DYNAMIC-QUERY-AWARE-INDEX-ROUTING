import pandas as pd
from pymongo import MongoClient

# --------------------------------------------------
# 1. Configuration
# --------------------------------------------------

DATA_FILE = "data/cleaned_taxi_data.parquet"

MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "dqi_project"
COLLECTION_NAME = "spatiotemporal_data"

BATCH_SIZE = 5000

# --------------------------------------------------
# 2. Connect to MongoDB
# --------------------------------------------------

print("Connecting to MongoDB...")

client = MongoClient(MONGO_URI)

db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

print("Connected successfully!")

# --------------------------------------------------
# 3. Load cleaned dataset
# --------------------------------------------------

print("\nLoading cleaned dataset...")

df = pd.read_parquet(DATA_FILE)

print("Records to import:", len(df))

# --------------------------------------------------
# 4. Convert records to MongoDB documents
# --------------------------------------------------

documents = []

for _, row in df.iterrows():

    document = {
        "taxi_id": int(row["taxi_id"]),

        "pickup_time": row["pickup_time"].to_pydatetime(),
        "dropoff_time": row["dropoff_time"].to_pydatetime(),

        "pickup_location": {
            "type": "Point",
            "coordinates": [
                float(row["pickup_longitude"]),
                float(row["pickup_latitude"])
            ]
        },

        "dropoff_location": {
            "type": "Point",
            "coordinates": [
                float(row["dropoff_longitude"]),
                float(row["dropoff_latitude"])
            ]
        },

        "pickup_location_id": int(row["pickup_location_id"]),
        "dropoff_location_id": int(row["dropoff_location_id"]),

        "passenger_count": float(row["passenger_count"]),
        "trip_distance": float(row["trip_distance"]),
        "fare_amount": float(row["fare_amount"])
    }

    documents.append(document)

    # Insert in batches
    if len(documents) >= BATCH_SIZE:

        collection.insert_many(
            documents,
            ordered=False
        )

        documents = []

        print(
            "Imported approximately",
            collection.count_documents({}),
            "documents"
        )

# --------------------------------------------------
# 5. Insert remaining documents
# --------------------------------------------------

if documents:

    collection.insert_many(
        documents,
        ordered=False
    )

# --------------------------------------------------
# 6. Final count
# --------------------------------------------------

final_count = collection.count_documents({})

print("\n========================================")
print("IMPORT COMPLETED")
print("========================================")

print("Documents in MongoDB:", final_count)

client.close()