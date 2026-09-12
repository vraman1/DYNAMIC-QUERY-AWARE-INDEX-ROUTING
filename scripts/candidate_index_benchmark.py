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
# Candidate indexes
# --------------------------------------------------

candidate_indexes = [

    "pickup_time_1",

    "pickup_location_2dsphere",

    "pickup_location_2dsphere_pickup_time_1"

]


# --------------------------------------------------
# Number of benchmark runs
# --------------------------------------------------

NUM_RUNS = 5


# --------------------------------------------------
# Results storage
# --------------------------------------------------

results = []


print("=" * 70)
print("CANDIDATE INDEX BENCHMARK")
print("=" * 70)

print("Total queries:", len(queries))

print(
    "Candidate indexes:",
    len(candidate_indexes)
)

print(
    "Runs per query/index:",
    NUM_RUNS
)

print(
    "Expected executions:",
    len(queries) *
    len(candidate_indexes) *
    NUM_RUNS
)


# --------------------------------------------------
# Execute every query with every candidate index
# --------------------------------------------------

for query in queries:

    query_id = query["query_id"]

    query_type = query["query_type"]


    print("\n" + "=" * 70)

    print(
        query_id,
        "|",
        query_type
    )

    print("=" * 70)


    for index_name in candidate_indexes:

        print(
            "\nTesting index:",
            index_name
        )


        for run_number in range(
            1,
            NUM_RUNS + 1
        ):

            # --------------------------------------------------
            # Force candidate index
            # --------------------------------------------------

            result = collection.find(
                query["filter"]
            ).hint(
                index_name
            ).explain()


            execution_stats = result[
                "executionStats"
            ]


            # --------------------------------------------------
            # Store measurements
            # --------------------------------------------------

            results.append({

                "query_id":
                    query_id,

                "query_type":
                    query_type,

                "run":
                    run_number,

                "index_used":
                    index_name,

                "results":
                    execution_stats[
                        "nReturned"
                    ],

                "execution_time_ms":
                    execution_stats[
                        "executionTimeMillis"
                    ],

                "documents_examined":
                    execution_stats[
                        "totalDocsExamined"
                    ],

                "keys_examined":
                    execution_stats[
                        "totalKeysExamined"
                    ]

            })


            print(
                f"Run {run_number} | "
                f"Time: "
                f"{execution_stats['executionTimeMillis']:5d} ms | "
                f"Results: "
                f"{execution_stats['nReturned']:6d} | "
                f"Docs: "
                f"{execution_stats['totalDocsExamined']:7d} | "
                f"Keys: "
                f"{execution_stats['totalKeysExamined']:7d}"
            )


# --------------------------------------------------
# Save benchmark results
# --------------------------------------------------

os.makedirs(
    "results",
    exist_ok=True
)


output_file = (
    "results/"
    "candidate_index_benchmark.csv"
)


fieldnames = [

    "query_id",

    "query_type",

    "run",

    "index_used",

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

print(
    "CANDIDATE INDEX BENCHMARK COMPLETED"
)

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