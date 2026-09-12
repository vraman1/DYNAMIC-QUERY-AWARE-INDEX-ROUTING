import pandas as pd


# ---------------------------------------------------------
# File paths
# ---------------------------------------------------------
native_file = "results/expanded_native_benchmark.csv"
router_file = "results/rule_router_benchmark_expanded.csv"
candidate_file = "results/candidate_index_analysis.csv"

output_file = "results/experimental_summary.csv"


# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------
native = pd.read_csv(native_file)
router = pd.read_csv(router_file)
candidate = pd.read_csv(candidate_file)


# ---------------------------------------------------------
# Verify input sizes
# ---------------------------------------------------------
print("\n=== INPUT DATA CHECK ===")

print(f"Native benchmark rows:     {len(native)}")
print(f"Router benchmark rows:     {len(router)}")
print(f"Candidate analysis rows:   {len(candidate)}")


# ---------------------------------------------------------
# 1. Native MongoDB performance
# ---------------------------------------------------------
native_summary = (
    native
    .groupby(["query_id", "query_type"])
    .agg(
        native_mean_time_ms=("execution_time_ms", "mean"),
        native_min_time_ms=("execution_time_ms", "min"),
        native_max_time_ms=("execution_time_ms", "max"),
        native_mean_documents_examined=(
            "documents_examined",
            "mean"
        ),
        native_mean_keys_examined=(
            "keys_examined",
            "mean"
        ),
        results=("results", "median")
    )
    .reset_index()
)


# ---------------------------------------------------------
# 2. Rule-based router performance
# ---------------------------------------------------------
router_summary = (
    router
    .groupby(
        ["query_id", "query_type", "selected_index"]
    )
    .agg(
        router_mean_time_ms=("execution_time_ms", "mean"),
        router_min_time_ms=("execution_time_ms", "min"),
        router_max_time_ms=("execution_time_ms", "max"),
        router_mean_documents_examined=(
            "documents_examined",
            "mean"
        ),
        router_mean_keys_examined=(
            "keys_examined",
            "mean"
        )
    )
    .reset_index()
)


# ---------------------------------------------------------
# 3. Empirical best-index results
# ---------------------------------------------------------
candidate_summary = candidate[
    [
        "query_id",
        "best_index",
        "best_mean_time_ms",
        "best_mean_documents_examined",
        "best_mean_keys_examined",
        "performance_gap_ms",
        "performance_gap_percent",
        "router_selected_best"
    ]
].copy()


# ---------------------------------------------------------
# 4. Combine native + router results
# ---------------------------------------------------------
summary = native_summary.merge(
    router_summary,
    on=["query_id", "query_type"],
    how="left"
)


# ---------------------------------------------------------
# 5. Add empirical best-index results
# ---------------------------------------------------------
summary = summary.merge(
    candidate_summary,
    on="query_id",
    how="left"
)


# ---------------------------------------------------------
# 6. Calculate router improvement over native MongoDB
# ---------------------------------------------------------
summary["router_improvement_percent"] = (
    (
        summary["native_mean_time_ms"]
        - summary["router_mean_time_ms"]
    )
    / summary["native_mean_time_ms"]
) * 100


# ---------------------------------------------------------
# 7. Calculate best-index improvement over native MongoDB
# ---------------------------------------------------------
summary["best_improvement_percent"] = (
    (
        summary["native_mean_time_ms"]
        - summary["best_mean_time_ms"]
    )
    / summary["native_mean_time_ms"]
) * 100


# ---------------------------------------------------------
# 8. Calculate document examination reduction
# ---------------------------------------------------------
summary["documents_reduction_percent"] = (
    (
        summary["native_mean_documents_examined"]
        - summary["router_mean_documents_examined"]
    )
    / summary["native_mean_documents_examined"]
) * 100


# ---------------------------------------------------------
# 9. Calculate key examination reduction
# ---------------------------------------------------------
summary["keys_reduction_percent"] = (
    (
        summary["native_mean_keys_examined"]
        - summary["router_mean_keys_examined"]
    )
    / summary["native_mean_keys_examined"]
) * 100


# ---------------------------------------------------------
# 10. Round numerical values
# ---------------------------------------------------------
numeric_columns = summary.select_dtypes(
    include=["float64", "float32"]
).columns

summary[numeric_columns] = (
    summary[numeric_columns].round(2)
)


# ---------------------------------------------------------
# 11. Sort queries logically
# ---------------------------------------------------------
query_order = [
    "T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9",
    "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9",
    "ST1", "ST2", "ST3", "ST4", "ST5", "ST6", "ST7", "ST8", "ST9",
    "TA1", "TA2", "TA3", "TA4", "TA5", "TA6", "TA7", "TA8", "TA9",
    "SA1", "SA2", "SA3", "SA4", "SA5", "SA6", "SA7", "SA8", "SA9",
    "STA1", "STA2", "STA3", "STA4", "STA5", "STA6", "STA7", "STA8", "STA9"
]

summary["query_order"] = summary["query_id"].map(
    {query_id: i for i, query_id in enumerate(query_order)}
)

summary = summary.sort_values("query_order")

summary = summary.drop(
    columns=["query_order"]
)


# ---------------------------------------------------------
# 12. Save consolidated results
# ---------------------------------------------------------
summary.to_csv(
    output_file,
    index=False
)


# ---------------------------------------------------------
# 13. Display main results
# ---------------------------------------------------------
display_columns = [
    "query_id",
    "query_type",
    "selected_index",
    "best_index",
    "results",
    "native_mean_time_ms",
    "router_mean_time_ms",
    "best_mean_time_ms",
    "router_improvement_percent",
    "best_improvement_percent",
    "documents_reduction_percent",
    "keys_reduction_percent",
    "router_selected_best"
]


print(
    "\n=== CONSOLIDATED EXPERIMENTAL RESULTS ===\n"
)

print(
    summary[display_columns].to_string(
        index=False
    )
)


# ---------------------------------------------------------
# 14. Overall workload statistics
# ---------------------------------------------------------
print(
    "\n=== OVERALL WORKLOAD RESULTS ==="
)


overall_native = (
    summary["native_mean_time_ms"].mean()
)

overall_router = (
    summary["router_mean_time_ms"].mean()
)

overall_best = (
    summary["best_mean_time_ms"].mean()
)


# ---------------------------------------------------------
# Router improvement over native
# ---------------------------------------------------------
overall_router_improvement = (
    (
        overall_native
        - overall_router
    )
    / overall_native
) * 100


# ---------------------------------------------------------
# Best-index improvement over native
# ---------------------------------------------------------
overall_best_improvement = (
    (
        overall_native
        - overall_best
    )
    / overall_native
) * 100


# ---------------------------------------------------------
# Router gap from empirical best
# ---------------------------------------------------------
overall_router_gap = (
    (
        overall_router
        - overall_best
    )
    / overall_best
) * 100


# ---------------------------------------------------------
# Document reduction
# ---------------------------------------------------------
documents_reduction = (
    (
        summary[
            "native_mean_documents_examined"
        ].mean()
        -
        summary[
            "router_mean_documents_examined"
        ].mean()
    )
    /
    summary[
        "native_mean_documents_examined"
    ].mean()
) * 100


# ---------------------------------------------------------
# Key reduction
# ---------------------------------------------------------
keys_reduction = (
    (
        summary[
            "native_mean_keys_examined"
        ].mean()
        -
        summary[
            "router_mean_keys_examined"
        ].mean()
    )
    /
    summary[
        "native_mean_keys_examined"
    ].mean()
) * 100


# ---------------------------------------------------------
# Routing accuracy
# ---------------------------------------------------------
correct_routes = (
    summary["router_selected_best"]
    .sum()
)

total_queries = len(summary)

accuracy = (
    correct_routes
    / total_queries
) * 100


# ---------------------------------------------------------
# Print overall results
# ---------------------------------------------------------
print(
    f"Total queries: {total_queries}"
)

print(
    f"Router selected best: "
    f"{int(correct_routes)}"
)

print(
    f"Routing accuracy: "
    f"{accuracy:.2f}%"
)

print(
    f"\nAverage native MongoDB time: "
    f"{overall_native:.2f} ms"
)

print(
    f"Average router time:         "
    f"{overall_router:.2f} ms"
)

print(
    f"Average best-index time:     "
    f"{overall_best:.2f} ms"
)

print(
    f"\nRouter improvement over native: "
    f"{overall_router_improvement:.2f}%"
)

print(
    f"Best-index improvement over native: "
    f"{overall_best_improvement:.2f}%"
)

print(
    f"Router performance gap from best: "
    f"{overall_router_gap:.2f}%"
)

print(
    f"\nAverage documents examined reduction: "
    f"{documents_reduction:.2f}%"
)

print(
    f"Average keys examined reduction:      "
    f"{keys_reduction:.2f}%"
)


# ---------------------------------------------------------
# Query-type level analysis
# ---------------------------------------------------------
print(
    "\n=== QUERY-TYPE PERFORMANCE ===\n"
)


type_summary = (
    summary
    .groupby("query_type")
    .agg(
        queries=("query_id", "count"),
        native_mean_ms=(
            "native_mean_time_ms",
            "mean"
        ),
        router_mean_ms=(
            "router_mean_time_ms",
            "mean"
        ),
        best_mean_ms=(
            "best_mean_time_ms",
            "mean"
        ),
        router_accuracy=(
            "router_selected_best",
            "mean"
        )
    )
    .reset_index()
)


type_summary["router_improvement_percent"] = (
    (
        type_summary["native_mean_ms"]
        -
        type_summary["router_mean_ms"]
    )
    /
    type_summary["native_mean_ms"]
) * 100


type_summary["router_accuracy"] = (
    type_summary["router_accuracy"] * 100
)


type_summary = type_summary.round(2)


print(
    type_summary.to_string(index=False)
)


# ---------------------------------------------------------
# Save query-type summary
# ---------------------------------------------------------
type_summary_file = (
    "results/query_type_summary.csv"
)

type_summary.to_csv(
    type_summary_file,
    index=False
)


# ---------------------------------------------------------
# Final message
# ---------------------------------------------------------
print(
    f"\nDetailed results saved to: "
    f"{output_file}"
)

print(
    f"Query-type summary saved to: "
    f"{type_summary_file}"
)