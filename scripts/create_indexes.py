from pymongo import MongoClient, ASCENDING, GEOSPHERE

# --------------------------------------------------
# 1. Configuration
# --------------------------------------------------

MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "dqi_project"
COLLECTION_NAME = "spatiotemporal_data"

# Candidate indexes used by the router and the backend
INDEXES = [
    {
        "name": "pickup_time_1",
        "keys": [("pickup_time", ASCENDING)],
        "label": "Temporal Index"
    },
    {
        "name": "pickup_location_2dsphere",
        "keys": [("pickup_location", GEOSPHERE)],
        "label": "Spatial Index"
    },
    {
        "name": "pickup_location_2dsphere_pickup_time_1",
        "keys": [
            ("pickup_location", GEOSPHERE),
            ("pickup_time", ASCENDING)
        ],
        "label": "Compound Spatial-Temporal Index"
    },
]

# --------------------------------------------------
# 2. Connect to MongoDB
# --------------------------------------------------

print("Connecting to MongoDB...")

client = MongoClient(MONGO_URI)

db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

document_count = collection.count_documents({})

print("Connected successfully!")
print("Documents in collection:", document_count)

if document_count == 0:
    print("\nCollection is empty. Run scripts/load_data.py first.")
    client.close()
    raise SystemExit(1)

# --------------------------------------------------
# 3. Create indexes
# --------------------------------------------------

# create_index is a no-op if the same index already exists,
# so this script is safe to run more than once.

existing = collection.index_information()

for index in INDEXES:

    if index["name"] in existing:
        print(f"\n[exists]  {index['label']}: {index['name']}")
        continue

    print(f"\n[create]  {index['label']}: {index['name']} ...")

    collection.create_index(
        index["keys"],
        name=index["name"]
    )

    print("          done")

# --------------------------------------------------
# 4. Verify
# --------------------------------------------------

print("\n========================================")
print("INDEXES ON", COLLECTION_NAME)
print("========================================")

for name, info in collection.index_information().items():
    print(f"- {name}: {info['key']}")

client.close()
