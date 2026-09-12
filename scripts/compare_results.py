import csv
import statistics
import os


# --------------------------------------------------
# Read CSV file
# --------------------------------------------------

def read_results(filename):

    results = []

    with open(filename, "r", newline="") as file:

        reader = csv.DictReader(file)

        for row in reader:

            row["execution_time_ms"] = float(
                row["execution_time_ms"]
            )

            results.append(row)

    return results


# --------------------------------------------------
# Calculate statistics
# --------------------------------------------------

def calculate_statistics(results):

    grouped = {}

    for row in results:

        query_id = row["query_id"]

        if query_id not in grouped:
            grouped[query_id] = []

        grouped[query_id].append(
            row["execution_time_ms"]
        )


    statistics_results = []


    for query_id, times in grouped.items():

        statistics_results.append({

            "query_id": query_id,

            "runs": len(times),

            "mean_ms": statistics.mean(times),

            "median_ms": statistics.median(times),

            "minimum_ms": min(times),

            "maximum_ms": max(times),

            "std_dev_ms":
                statistics.stdev(times)
                if len(times) > 1
                else 0

        })


    return statistics_results


# --------------------------------------------------
# Read benchmark files
# --------------------------------------------------

normal_results = read_results(
    "results/repeated_benchmark.csv"
)

router_results = read_results(
    "results/rule_router_benchmark.csv"
)


# --------------------------------------------------
# Calculate statistics
# --------------------------------------------------

normal_stats = calculate_statistics(
    normal_results
)

router_stats = calculate_statistics(
    router_results
)


# --------------------------------------------------
# Combine results
# --------------------------------------------------

comparison = []


for normal in normal_stats:

    query_id = normal["query_id"]

    router = next(
        item for item in router_stats
        if item["query_id"] == query_id
    )


    normal_mean = normal["mean_ms"]

    router_mean = router["mean_ms"]


    # --------------------------------------------------
    # Percentage improvement
    # --------------------------------------------------

    improvement = (
        (normal_mean - router_mean)
        / normal_mean
    ) * 100


    comparison.append({

        "query_id": query_id,

        "normal_mean_ms":
            round(normal_mean, 3),

        "normal_median_ms":
            round(normal["median_ms"], 3),

        "normal_min_ms":
            round(normal["minimum_ms"], 3),

        "normal_max_ms":
            round(normal["maximum_ms"], 3),

        "normal_std_dev_ms":
            round(normal["std_dev_ms"], 3),

        "router_mean_ms":
            round(router_mean, 3),

        "router_median_ms":
            round(router["median_ms"], 3),

        "router_min_ms":
            round(router["minimum_ms"], 3),

        "router_max_ms":
            round(router["maximum_ms"], 3),

        "router_std_dev_ms":
            round(router["std_dev_ms"], 3),

        "improvement_percent":
            round(improvement, 2)

    })


# --------------------------------------------------
# Print comparison
# --------------------------------------------------

print("=" * 100)
print("MONGODB vs RULE-BASED ROUTER")
print("=" * 100)


for row in comparison:

    print("\nQuery:", row["query_id"])

    print(
        "Normal MongoDB Mean:",
        row["normal_mean_ms"],
        "ms"
    )

    print(
        "Rule Router Mean:",
        row["router_mean_ms"],
        "ms"
    )

    print(
        "Improvement:",
        row["improvement_percent"],
        "%"
    )

    print(
        "Normal Median:",
        row["normal_median_ms"],
        "ms"
    )

    print(
        "Router Median:",
        row["router_median_ms"],
        "ms"
    )

    print(
        "Normal Std Dev:",
        row["normal_std_dev_ms"],
        "ms"
    )

    print(
        "Router Std Dev:",
        row["router_std_dev_ms"],
        "ms"
    )


# --------------------------------------------------
# Save comparison
# --------------------------------------------------

os.makedirs("results", exist_ok=True)

output_file = "results/mongodb_vs_rule_router.csv"


fieldnames = list(comparison[0].keys())


with open(
    output_file,
    "w",
    newline=""
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=fieldnames
    )

    writer.writeheader()

    writer.writerows(comparison)


# --------------------------------------------------
# Finish
# --------------------------------------------------

print("\n" + "=" * 100)
print("COMPARISON COMPLETED")
print("=" * 100)

print(
    "\nComparison saved to:",
    output_file
)