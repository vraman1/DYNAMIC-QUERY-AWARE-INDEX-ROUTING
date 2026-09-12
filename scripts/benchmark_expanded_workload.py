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
# Number of runs
# --------------------------------------------------

NUM_RUNS = 5


# --------------------------------------------------
# Results storage
# --------------------------------------------------

results = []


print("=" * 80)
print("EXPANDED WORKLOAD BENCHMARK")
print("=" * 80)

print("Total queries:", len(queries))
print("Runs per query:", NUM_RUNS)


# --------------------------------------------------
# Execute workload
# --------------------------------------------------

for query in queries:

    query_id = query["query_id"]

    query_type = query["query_type"]

    description = query["description"]


    print("\n" + "-" * 80)

    print(
        query_id,
        "|",
        query_type,
        "|",
        description
    )

    print("-" * 80)


    for run_number in range(1, NUM_RUNS + 1):

        # --------------------------------------------------
        # Execute query
        # --------------------------------------------------

        result = collection.find(
            query["filter"]
        ).explain()


        execution_stats = result["executionStats"]

        winning_plan = result["queryPlanner"]["winningPlan"]


        # --------------------------------------------------
        # Find selected index
        # --------------------------------------------------

        index_used = None


        def find_index(stage):

            if isinstance(stage, dict):

                if "indexName" in stage:
                    return stage["indexName"]

                for value in stage.values():

                    found = find_index(value)

                    if found:
                        return found


            elif isinstance(stage, list):

                for item in stage:

                    found = find_index(item)

                    if found:
                        return found


            return None


        index_used = find_index(winning_plan)


        # --------------------------------------------------
        # Store results
        # --------------------------------------------------

        results.append({

            "query_id": query_id,

            "query_type": query_type,

            "description": description,

            "run": run_number,

            "results":
                execution_stats["nReturned"],

            "execution_time_ms":
                execution_stats["executionTimeMillis"],

            "documents_examined":
                execution_stats["totalDocsExamined"],

            "keys_examined":
                execution_stats["totalKeysExamined"],

            "index_used":
                index_used

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
            f"{execution_stats['totalKeysExamined']:6d} | "
            f"Index: "
            f"{index_used}"
        )


# --------------------------------------------------
# Save results
# --------------------------------------------------

os.makedirs("results", exist_ok=True)

output_file = (
    "results/expanded_workload_benchmark.csv"
)


fieldnames = [

    "query_id",

    "query_type",

    "description",

    "run",

    "results",

    "execution_time_ms",

    "documents_examined",

    "keys_examined",

    "index_used"
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

print("\n" + "=" * 80)
print("EXPANDED WORKLOAD BENCHMARK COMPLETED")
print("=" * 80)

print(
    "\nTotal executions:",
    len(results)
)

print(
    "Results saved to:",
    output_file
)


client.close()