import time
import pandas as pd
from pymongo import MongoClient

from generate_workload import queries


# ---------------------------------------------------------
# MongoDB connection
# ---------------------------------------------------------
client = MongoClient("mongodb://localhost:27017/")

db = client["dqi_project"]
collection = db["spatiotemporal_data"]


# ---------------------------------------------------------
# Settings
# ---------------------------------------------------------
NUM_RUNS = 5

output_file = "results/expanded_native_benchmark.csv"


# ---------------------------------------------------------
# Benchmark
# ---------------------------------------------------------
results = []


print("=" * 70)
print("EXPANDED NATIVE MONGODB QUERY BENCHMARK")
print("=" * 70)

print(f"Total queries: {len(queries)}")
print(f"Runs per query: {NUM_RUNS}")
print(f"Total executions: {len(queries) * NUM_RUNS}")


for query in queries:

    query_id = query["query_id"]
    query_type = query["query_type"]
    query_filter = query["filter"]

    print("\n" + "-" * 70)
    print(f"{query_id} | {query_type}")
    print("-" * 70)

    for run in range(1, NUM_RUNS + 1):

        # -------------------------------------------------
        # Execute with MongoDB's normal query optimizer
        # -------------------------------------------------
        start_time = time.perf_counter()

        explanation = collection.find(
            query_filter
        ).explain()

        end_time = time.perf_counter()

        execution_time_ms = (
            end_time - start_time
        ) * 1000

        # -------------------------------------------------
        # Extract execution statistics
        # -------------------------------------------------
        execution_stats = explanation["executionStats"]

        results_count = execution_stats[
            "nReturned"
        ]

        documents_examined = execution_stats[
            "totalDocsExamined"
        ]

        keys_examined = execution_stats[
            "totalKeysExamined"
        ]

        # -------------------------------------------------
        # Determine winning plan / index
        # -------------------------------------------------
        winning_plan = explanation[
            "queryPlanner"
        ]["winningPlan"]

        index_used = "COLLSCAN"

        def find_index(plan):

            if not isinstance(plan, dict):
                return None

            if plan.get("stage") == "IXSCAN":
                return plan.get(
                    "indexName"
                )

            if "inputStage" in plan:
                result = find_index(
                    plan["inputStage"]
                )

                if result:
                    return result

            if "inputStages" in plan:
                for stage in plan["inputStages"]:

                    result = find_index(stage)

                    if result:
                        return result

            if "shards" in plan:
                for shard in plan["shards"]:

                    result = find_index(
                        shard.get("winningPlan", {})
                    )

                    if result:
                        return result

            return None

        detected_index = find_index(
            winning_plan
        )

        if detected_index:
            index_used = detected_index

        print(
            f"Run {run:2d} | "
            f"Time: {execution_time_ms:7.2f} ms | "
            f"Results: {results_count:6d} | "
            f"Docs: {documents_examined:7d} | "
            f"Keys: {keys_examined:7d} | "
            f"Index: {index_used}"
        )

        results.append({
            "query_id": query_id,
            "query_type": query_type,
            "run": run,
            "results": results_count,
            "execution_time_ms":
                execution_time_ms,
            "documents_examined":
                documents_examined,
            "keys_examined":
                keys_examined,
            "index_used": index_used
        })


# ---------------------------------------------------------
# Save results
# ---------------------------------------------------------
results_df = pd.DataFrame(results)

results_df.to_csv(
    output_file,
    index=False
)


print("\n" + "=" * 70)
print("EXPANDED NATIVE BENCHMARK COMPLETED")
print("=" * 70)

print(
    f"Total executions: {len(results_df)}"
)

print(
    f"Expected executions: "
    f"{len(queries) * NUM_RUNS}"
)

print(
    f"Results saved to: {output_file}"
)