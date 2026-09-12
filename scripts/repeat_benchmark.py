from pymongo import MongoClient
from datetime import datetime
import csv
import os
import time


# --------------------------------------------------
# MongoDB connection
# --------------------------------------------------

client = MongoClient("mongodb://localhost:27017/")

db = client["dqi_project"]
collection = db["spatiotemporal_data"]


# --------------------------------------------------
# Number of repetitions
# --------------------------------------------------

NUM_RUNS = 10


# --------------------------------------------------
# Query definitions
# --------------------------------------------------

queries = [

    # Q1 - Temporal
    {
        "query_id": "Q1",
        "query_type": "temporal",
        "filter": {
            "pickup_time": {
                "$gte": datetime(2026, 1, 1, 10, 0, 0),
                "$lt": datetime(2026, 1, 1, 11, 0, 0)
            }
        }
    },

    # Q2 - Spatial
    {
        "query_id": "Q2",
        "query_type": "spatial",
        "filter": {
            "pickup_location": {
                "$geoWithin": {
                    "$centerSphere": [
                        [-73.9857, 40.7484],
                        1 / 6378.1
                    ]
                }
            }
        }
    },

    # Q3 - Spatio-temporal
    {
        "query_id": "Q3",
        "query_type": "spatio_temporal",
        "filter": {
            "pickup_time": {
                "$gte": datetime(2026, 1, 1, 10, 0, 0),
                "$lt": datetime(2026, 1, 1, 11, 0, 0)
            },
            "pickup_location": {
                "$geoWithin": {
                    "$centerSphere": [
                        [-73.9857, 40.7484],
                        1 / 6378.1
                    ]
                }
            }
        }
    },

    # Q4 - Temporal + Attribute
    {
        "query_id": "Q4",
        "query_type": "temporal_attribute",
        "filter": {
            "pickup_time": {
                "$gte": datetime(2026, 1, 1, 10, 0, 0),
                "$lt": datetime(2026, 1, 1, 11, 0, 0)
            },
            "passenger_count": {
                "$gte": 2
            }
        }
    },

    # Q5 - Spatial + Attribute
    {
        "query_id": "Q5",
        "query_type": "spatial_attribute",
        "filter": {
            "pickup_location": {
                "$geoWithin": {
                    "$centerSphere": [
                        [-73.9857, 40.7484],
                        1 / 6378.1
                    ]
                }
            },
            "trip_distance": {
                "$gt": 2
            }
        }
    },

    # Q6 - Spatio-temporal + Attribute
    {
        "query_id": "Q6",
        "query_type": "spatio_temporal_attribute",
        "filter": {
            "pickup_time": {
                "$gte": datetime(2026, 1, 1, 10, 0, 0),
                "$lt": datetime(2026, 1, 1, 11, 0, 0)
            },
            "pickup_location": {
                "$geoWithin": {
                    "$centerSphere": [
                        [-73.9857, 40.7484],
                        1 / 6378.1
                    ]
                }
            },
            "passenger_count": {
                "$gte": 2
            }
        }
    }
]


# --------------------------------------------------
# Results storage
# --------------------------------------------------

results = []


print("=" * 70)
print("REPEATED QUERY BENCHMARK")
print("=" * 70)

print("Number of runs per query:", NUM_RUNS)


# --------------------------------------------------
# Execute each query multiple times
# --------------------------------------------------

for query in queries:

    print("\n" + "-" * 70)
    print(
        query["query_id"],
        "-",
        query["query_type"]
    )
    print("-" * 70)

    for run_number in range(1, NUM_RUNS + 1):

        result = collection.find(
            query["filter"]
        ).explain()

        execution_stats = result["executionStats"]
        winning_plan = result["queryPlanner"]["winningPlan"]


        # --------------------------------------------------
        # Find index used
        # --------------------------------------------------

        index_used = None

        if "inputStage" in winning_plan:

            input_stage = winning_plan["inputStage"]

            if "indexName" in input_stage:
                index_used = input_stage["indexName"]


        # --------------------------------------------------
        # Store result
        # --------------------------------------------------

        results.append({

            "query_id": query["query_id"],

            "query_type": query["query_type"],

            "run": run_number,

            "results": execution_stats["nReturned"],

            "execution_time_ms":
                execution_stats["executionTimeMillis"],

            "documents_examined":
                execution_stats["totalDocsExamined"],

            "keys_examined":
                execution_stats["totalKeysExamined"],

            "index_used": index_used

        })


        print(
            f"Run {run_number:2d} | "
            f"Time: {execution_stats['executionTimeMillis']:4d} ms | "
            f"Docs: {execution_stats['totalDocsExamined']:6d} | "
            f"Keys: {execution_stats['totalKeysExamined']:6d} | "
            f"Index: {index_used}"
        )


# --------------------------------------------------
# Save results
# --------------------------------------------------

os.makedirs("results", exist_ok=True)

output_file = "results/repeated_benchmark.csv"


with open(
    output_file,
    "w",
    newline=""
) as file:

    fieldnames = [
        "query_id",
        "query_type",
        "run",
        "results",
        "execution_time_ms",
        "documents_examined",
        "keys_examined",
        "index_used"
    ]

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
print("REPEATED BENCHMARK COMPLETED")
print("=" * 70)

print(
    "\nResults saved to:",
    output_file
)


client.close()