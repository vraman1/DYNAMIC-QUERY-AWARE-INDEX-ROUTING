import pandas as pd
from generate_workload import queries


# ---------------------------------------------------------
# File paths
# ---------------------------------------------------------
benchmark_file = "results/candidate_index_benchmark.csv"
output_file = "results/query_features_expanded.csv"


# ---------------------------------------------------------
# Load candidate benchmark
# ---------------------------------------------------------
benchmark = pd.read_csv(benchmark_file)


# ---------------------------------------------------------
# Get actual result size for each query
#
# Result size is independent of which candidate index
# is used, so we take the median across all benchmark runs.
# ---------------------------------------------------------
result_sizes = (
    benchmark
    .groupby("query_id")["results"]
    .median()
    .to_dict()
)


# ---------------------------------------------------------
# Total documents in MongoDB
# ---------------------------------------------------------
total_documents = 495160


# ---------------------------------------------------------
# Feature extraction
# ---------------------------------------------------------
def extract_features(
    query_id,
    query_type,
    query_filter,
    result_size
):
    spatial_query = 0
    temporal_query = 0
    attribute_query = 0
    has_2dsphere = 0
    has_time_filter = 0
    number_of_filters = 0

    # Spatial feature
    if "pickup_location" in query_filter:
        spatial_query = 1
        has_2dsphere = 1
        number_of_filters += 1

    # Temporal feature
    if "pickup_time" in query_filter:
        temporal_query = 1
        has_time_filter = 1
        number_of_filters += 1

    # Attribute features
    if "passenger_count" in query_filter:
        attribute_query = 1
        number_of_filters += 1

    if "trip_distance" in query_filter:
        attribute_query = 1
        number_of_filters += 1

    # Query selectivity
    query_selectivity = result_size / total_documents

    return {
        "query_id": query_id,
        "query_type": query_type,
        "spatial_query": spatial_query,
        "temporal_query": temporal_query,
        "attribute_query": attribute_query,
        "has_2dsphere": has_2dsphere,
        "has_time_filter": has_time_filter,
        "number_of_filters": number_of_filters,
        "result_size": result_size,
        "query_selectivity": query_selectivity
    }


# ---------------------------------------------------------
# Generate features for all queries
# ---------------------------------------------------------
feature_rows = []


for query in queries:

    query_id = query["query_id"]
    query_type = query["query_type"]
    query_filter = query["filter"]

    if query_id not in result_sizes:
        raise ValueError(
            f"No benchmark result found for query {query_id}"
        )

    result_size = int(result_sizes[query_id])

    features = extract_features(
        query_id,
        query_type,
        query_filter,
        result_size
    )

    feature_rows.append(features)

    print("\n" + "-" * 70)
    print(f"{query_id} - {query_type}")
    print("-" * 70)

    for key, value in features.items():
        if key not in ["query_id", "query_type"]:
            print(f"{key:25}: {value}")


# ---------------------------------------------------------
# Create DataFrame
# ---------------------------------------------------------
features_df = pd.DataFrame(feature_rows)


# ---------------------------------------------------------
# Save
# ---------------------------------------------------------
features_df.to_csv(
    output_file,
    index=False
)


# ---------------------------------------------------------
# Final verification
# ---------------------------------------------------------
print("\n" + "=" * 70)
print("FEATURE EXTRACTION COMPLETE")
print("=" * 70)

print(f"Total queries: {len(features_df)}")
print(f"Expected queries: {len(queries)}")

print("\nFeature columns:")
print(features_df.columns.tolist())

print(
    f"\nFeatures saved to: {output_file}"
)