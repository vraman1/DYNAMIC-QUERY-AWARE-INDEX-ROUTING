import csv


# --------------------------------------------------
# Rule-Based Index Router
# --------------------------------------------------

def route_query(features):
    """
    Select an index based on query features.
    """

    spatial = features["spatial_query"]
    temporal = features["temporal_query"]
    attribute = features["attribute_query"]


    # --------------------------------------------------
    # Rule 1: Spatial + Temporal + Attribute
    # --------------------------------------------------

    if spatial == 1 and temporal == 1 and attribute == 1:

        return "pickup_location_2dsphere_pickup_time_1"


    # --------------------------------------------------
    # Rule 2: Spatial + Temporal
    # --------------------------------------------------

    if spatial == 1 and temporal == 1:

        return "pickup_location_2dsphere_pickup_time_1"


    # --------------------------------------------------
    # Rule 3: Spatial + Attribute
    # --------------------------------------------------

    if spatial == 1 and temporal == 0 and attribute == 1:

        return "pickup_location_2dsphere"


    # --------------------------------------------------
    # Rule 4: Spatial only
    # --------------------------------------------------

    if spatial == 1 and temporal == 0 and attribute == 0:

        return "pickup_location_2dsphere"


    # --------------------------------------------------
    # Rule 5: Temporal + Attribute
    # --------------------------------------------------

    if temporal == 1 and spatial == 0:

        return "pickup_time_1"


    # --------------------------------------------------
    # Rule 6: Temporal only
    # --------------------------------------------------

    if temporal == 1:

        return "pickup_time_1"


    # --------------------------------------------------
    # No matching rule
    # --------------------------------------------------

    return "NO_INDEX"


# --------------------------------------------------
# Read expanded query features
# --------------------------------------------------

input_file = "results/query_features_expanded.csv"

features = []


with open(
    input_file,
    "r",
    newline=""
) as file:

    reader = csv.DictReader(file)

    for row in reader:

        # Convert numeric values
        row["spatial_query"] = int(row["spatial_query"])
        row["temporal_query"] = int(row["temporal_query"])
        row["attribute_query"] = int(row["attribute_query"])

        features.append(row)


# --------------------------------------------------
# Apply routing rules
# --------------------------------------------------

routing_results = []


print("=" * 70)
print("EXPANDED RULE-BASED INDEX ROUTER")
print("=" * 70)


for row in features:

    recommended_index = route_query(row)

    routing_results.append({

        "query_id": row["query_id"],

        "query_type": row["query_type"],

        "recommended_index": recommended_index

    })


    print("\nQuery ID:", row["query_id"])
    print("Query Type:", row["query_type"])
    print("Recommended Index:", recommended_index)


# --------------------------------------------------
# Save routing decisions
# --------------------------------------------------

output_file = "results/routing_decisions_expanded.csv"


with open(
    output_file,
    "w",
    newline=""
) as file:

    fieldnames = [
        "query_id",
        "query_type",
        "recommended_index"
    ]

    writer = csv.DictWriter(
        file,
        fieldnames=fieldnames
    )

    writer.writeheader()

    writer.writerows(routing_results)


# --------------------------------------------------
# Finish
# --------------------------------------------------

print("\n" + "=" * 70)
print("ROUTING COMPLETED")
print("=" * 70)

print("\nTotal queries routed:", len(routing_results))
print("Routing decisions saved to:", output_file)