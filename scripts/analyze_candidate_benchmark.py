import pandas as pd


# ---------------------------------------------------------
# File paths
# ---------------------------------------------------------
candidate_file = "results/candidate_index_benchmark.csv"
routing_file = "results/routing_decisions_expanded.csv"
router_benchmark_file = "results/rule_router_benchmark_expanded.csv"

output_file = "results/candidate_index_analysis.csv"


# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------
candidate = pd.read_csv(candidate_file)
routing = pd.read_csv(routing_file)
router_benchmark = pd.read_csv(router_benchmark_file)


# ---------------------------------------------------------
# Candidate index statistics
# ---------------------------------------------------------
candidate_summary = (
    candidate
    .groupby(
        ["query_id", "query_type", "index_used"]
    )
    .agg(
        mean_time_ms=("execution_time_ms", "mean"),
        mean_documents_examined=("documents_examined", "mean"),
        mean_keys_examined=("keys_examined", "mean")
    )
    .reset_index()
)


# ---------------------------------------------------------
# Find empirically best index
# ---------------------------------------------------------
best = (
    candidate_summary
    .loc[
        candidate_summary.groupby("query_id")[
            "mean_time_ms"
        ].idxmin()
    ]
    .copy()
)


best = best.rename(
    columns={
        "index_used": "best_index",
        "mean_time_ms": "best_mean_time_ms",
        "mean_documents_examined":
            "best_mean_documents_examined",
        "mean_keys_examined":
            "best_mean_keys_examined"
    }
)


# ---------------------------------------------------------
# Calculate actual router performance
# ---------------------------------------------------------
router_summary = (
    router_benchmark
    .groupby("query_id")
    .agg(
        router_mean_time_ms=("execution_time_ms", "mean"),
        router_mean_documents_examined=
            ("documents_examined", "mean"),
        router_mean_keys_examined=
            ("keys_examined", "mean")
    )
    .reset_index()
)


# ---------------------------------------------------------
# Get router's selected index
# ---------------------------------------------------------
router_choice = (
    routing[
        ["query_id", "recommended_index"]
    ]
    .drop_duplicates("query_id")
)


# ---------------------------------------------------------
# Merge everything
# ---------------------------------------------------------
analysis = (
    best
    .merge(
        router_choice,
        on="query_id",
        how="left"
    )
    .merge(
        router_summary,
        on="query_id",
        how="left"
    )
)


# ---------------------------------------------------------
# Check whether router selected empirical best
# ---------------------------------------------------------
analysis["router_selected_best"] = (
    analysis["recommended_index"]
    == analysis["best_index"]
)


# ---------------------------------------------------------
# Performance gap
# ---------------------------------------------------------
analysis["performance_gap_ms"] = (
    analysis["router_mean_time_ms"]
    - analysis["best_mean_time_ms"]
)


analysis["performance_gap_percent"] = (
    analysis["performance_gap_ms"]
    / analysis["best_mean_time_ms"]
    * 100
)


# ---------------------------------------------------------
# Save
# ---------------------------------------------------------
analysis = analysis.sort_values("query_id")

analysis.to_csv(
    output_file,
    index=False
)


# ---------------------------------------------------------
# Display
# ---------------------------------------------------------
print("\n=== ROUTER VS EMPIRICAL BEST INDEX ===\n")

display_columns = [
    "query_id",
    "query_type",
    "recommended_index",
    "best_index",
    "router_mean_time_ms",
    "best_mean_time_ms",
    "performance_gap_ms",
    "performance_gap_percent",
    "router_selected_best"
]

print(
    analysis[display_columns].to_string(
        index=False
    )
)


# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------
total_queries = len(analysis)

correct = analysis["router_selected_best"].sum()

accuracy = (
    correct / total_queries * 100
)


print("\n=== SUMMARY ===")

print(f"Total queries: {total_queries}")
print(f"Router selected best: {correct}")
print(f"Routing accuracy: {accuracy:.2f}%")


print(
    "\nAverage router execution time: "
    f"{analysis['router_mean_time_ms'].mean():.2f} ms"
)

print(
    "Average best-index execution time: "
    f"{analysis['best_mean_time_ms'].mean():.2f} ms"
)

print(
    "Average performance gap: "
    f"{analysis['performance_gap_ms'].mean():.2f} ms"
)

print(
    "Average performance gap (%): "
    f"{analysis['performance_gap_percent'].mean():.2f}%"
)


print(
    "\nAnalysis saved to: "
    f"{output_file}"
)