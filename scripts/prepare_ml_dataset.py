import pandas as pd

# ---------------------------------------------------------
# Input files
# ---------------------------------------------------------
features_file = "results/query_features_expanded.csv"
candidate_file = "results/candidate_index_benchmark.csv"

output_file = "results/ml_training_dataset.csv"


# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------
features = pd.read_csv(features_file)
candidate = pd.read_csv(candidate_file)


# ---------------------------------------------------------
# Calculate mean execution time for each
# query + candidate index
# ---------------------------------------------------------
performance = (
    candidate
    .groupby(["query_id", "index_used"])
    .agg(
        mean_execution_time_ms=("execution_time_ms", "mean")
    )
    .reset_index()
)


# ---------------------------------------------------------
# Find the empirically fastest index for each query
# ---------------------------------------------------------
best_indices = (
    performance
    .loc[
        performance.groupby("query_id")[
            "mean_execution_time_ms"
        ].idxmin()
    ]
    [["query_id", "index_used"]]
    .rename(columns={
        "index_used": "best_index"
    })
)


# ---------------------------------------------------------
# Combine query features with measured best index
# ---------------------------------------------------------
ml_dataset = features.merge(
    best_indices,
    on="query_id",
    how="inner"
)


# ---------------------------------------------------------
# Select ML features
# ---------------------------------------------------------
feature_columns = [
    "spatial_query",
    "temporal_query",
    "attribute_query",
    "has_2dsphere",
    "has_time_filter",
    "number_of_filters",
    "query_selectivity"
]

ml_dataset = ml_dataset[
    [
        "query_id",
        "query_type"
    ]
    + feature_columns
    + ["result_size", "best_index"]
]


# ---------------------------------------------------------
# Save dataset
# ---------------------------------------------------------
ml_dataset.to_csv(
    output_file,
    index=False
)


# ---------------------------------------------------------
# Display dataset
# ---------------------------------------------------------
print("\n=== ML TRAINING DATASET ===\n")

print(
    ml_dataset.to_string(index=False)
)


# ---------------------------------------------------------
# Display label distribution
# ---------------------------------------------------------
print("\n=== BEST INDEX DISTRIBUTION ===\n")

print(
    ml_dataset["best_index"]
    .value_counts()
    .to_string()
)


# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------
print("\n=== DATASET SUMMARY ===")

print(f"Total samples: {len(ml_dataset)}")
print(f"Number of features: {len(feature_columns)}")
print(
    f"Number of classes: "
    f"{ml_dataset['best_index'].nunique()}"
)

print(f"\nDataset saved to: {output_file}")