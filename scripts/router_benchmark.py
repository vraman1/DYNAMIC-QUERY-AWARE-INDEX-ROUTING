from pymongo import MongoClient
import csv
import os

from generate_workload import queries


# --------------------------------------------------
# MongoDB connection
# --------------------------------------------------

client = MongoClient("mongodb://localhost:27017/")

db = client["dqi_project"]
collection = db["spatiotemporal_data"]


# --------------------------------------------------
# Read routing decisions
# --------------------------------------------------

routing_file = "results/routing_decisions_expanded.csv"

routing_decisions = {}


with open(
    routing_file,
    "r",
    newline=""
) as file:

    reader = csv.DictReader(file)

    for row in reader:

        routing_decisions[row["query_id"]] = row["recommended_index"]


# --------------------------------------------------
# Number of benchmark runs
# --------------------------------------------------

NUM_RUNS = 5


# --------------------------------------------------
# Results storage
# --------------------------------------------------

results = []


print("=" * 70)
print("EXPANDED RULE-BASED ROUTER BENCHMARK")
print("=" * 70)

print("Total queries:", len(queries))
print("Runs per query:", NUM_RUNS)


# --------------------------------------------------
# Execute queries using router-selected indexes
# --------------------------------------------------

for query in queries:

    query_id = query["query_id"]

    query_type = query["query_type"]

    selected_index = routing_decisions[query_id]


    print("\n" + "-" * 70)

    print(
        query_id,
        "|",
        query_type
    )

    print(
        "Router selected:",
        selected_index
    )

    print("-" * 70)


    for run_number in range(1, NUM_RUNS + 1):

        # --------------------------------------------------
        # Force the router-selected index
        # --------------------------------------------------

        result = collection.find(
            query["filter"]
        ).hint(
            selected_index
        ).explain()


        execution_stats = result["executionStats"]


        # --------------------------------------------------
        # Store result
        # --------------------------------------------------

        results.append({

            "query_id":
                query_id,

            "query_type":
                query_type,

            "run":
                run_number,

            "selected_index":
                selected_index,

            "results":
                execution_stats["nReturned"],

            "execution_time_ms":
                execution_stats["executionTimeMillis"],

            "documents_examined":
                execution_stats["totalDocsExamined"],

            "keys_examined":
                execution_stats["totalKeysExamined"]

        })


        print(
            f"Run {run_number:2d} | "
            f"Time: "
            f"{execution_stats['executionTimeMillis']:5d} ms | "
            f"Results: "
            f"{execution_stats['nReturned']:6d} | "
            f"Docs: "
            f"{execution_stats['totalDocsExamined']:6d} | "
            f"Keys: "
            f"{execution_stats['totalKeysExamined']:6d}"
        )


# --------------------------------------------------
# Save results
# --------------------------------------------------

os.makedirs(
    "results",
    exist_ok=True
)


output_file = "results/rule_router_benchmark_expanded.csv"


fieldnames = [

    "query_id",

    "query_type",

    "run",

    "selected_index",

    "results",

    "execution_time_ms",

    "documents_examined",

    "keys_examined"

]


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

    writer.writerows(results)


# --------------------------------------------------
# Finish
# --------------------------------------------------

print("\n" + "=" * 70)
print("EXPANDED RULE-BASED ROUTER BENCHMARK COMPLETED")
print("=" * 70)

print(
    "\nTotal executions:",
    len(results)
)

print(
    "Results saved to:",
    output_file
)


client.close()