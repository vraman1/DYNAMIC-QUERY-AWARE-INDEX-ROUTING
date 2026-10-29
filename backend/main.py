from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from datetime import datetime, timezone
import time


# =========================================================
# FastAPI Application
# =========================================================

app = FastAPI(title="DQI Project API")


# =========================================================
# CORS Configuration
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# MongoDB Connection
# =========================================================

client = MongoClient("mongodb://localhost:27017/")

db = client["dqi_project"]

collection = db["spatiotemporal_data"]


# =========================================================
# Common Query Components
# =========================================================

temporal_filter = {
    "pickup_time": {
        "$gte": datetime(
            2026,
            1,
            1,
            10,
            0,
            0,
            tzinfo=timezone.utc
        ),
        "$lt": datetime(
            2026,
            1,
            1,
            11,
            0,
            0,
            tzinfo=timezone.utc
        )
    }
}


spatial_filter = {
    "pickup_location": {
        "$geoWithin": {
            "$centerSphere": [
                [-73.9857, 40.7484],
                1 / 6378.1
            ]
        }
    }
}


# =========================================================
# Root Endpoint
# =========================================================

@app.get("/")
def root():

    return {
        "message": "Dynamic Query-Aware Index Routing API is running"
    }


# =========================================================
# MongoDB Health Check
# =========================================================

@app.get("/api/health")
def health():

    try:

        client.admin.command("ping")

        document_count = collection.count_documents({})

        return {
            "status": "ok",
            "mongodb": "connected",
            "database": "dqi_project",
            "collection": "spatiotemporal_data",
            "documents": document_count
        }

    except Exception as e:

        return {
            "status": "error",
            "mongodb": "disconnected",
            "message": str(e)
        }


# =========================================================
# Rule-Based Index Router
# =========================================================

@app.post("/api/route")
def route_query(query_type: str):

    routes = {

        "Temporal":
            "pickup_time_1",

        "Spatial":
            "pickup_location_2dsphere",

        "Spatio-temporal":
            "pickup_location_2dsphere_pickup_time_1",

        "Temporal + Attribute":
            "pickup_time_1",

        "Spatial + Attribute":
            "pickup_location_2dsphere",

        "Spatio-temporal + Attribute":
            "pickup_location_2dsphere_pickup_time_1",
    }

    selected_index = routes.get(query_type)

    if selected_index is None:

        raise HTTPException(
            status_code=400,
            detail=f"Unknown query type: {query_type}"
        )

    return {
        "status": "ok",
        "query_type": query_type,
        "recommended_index": selected_index
    }


# =========================================================
# Execute Real MongoDB Query
# =========================================================

@app.post("/api/execute")
def execute_query(query_type: str):

    # -----------------------------------------------------
    # Query Definitions
    # -----------------------------------------------------

    queries = {

        # Q1 - Temporal
        "Temporal":
            temporal_filter,


        # Q2 - Spatial
        "Spatial":
            spatial_filter,


        # Q3 - Spatio-temporal
        "Spatio-temporal": {

            **temporal_filter,
            **spatial_filter

        },


        # Q4 - Temporal + Attribute
        "Temporal + Attribute": {

            **temporal_filter,

            "passenger_count": {
                "$gte": 2
            }

        },


        # Q5 - Spatial + Attribute
        "Spatial + Attribute": {

            **spatial_filter,

            "trip_distance": {
                "$gt": 2
            }

        },


        # Q6 - Spatio-temporal + Attribute
        "Spatio-temporal + Attribute": {

            **temporal_filter,
            **spatial_filter,

            "passenger_count": {
                "$gte": 2
            }

        }
    }


    # -----------------------------------------------------
    # Index Definitions
    # -----------------------------------------------------

    indexes = {

        "Temporal":
            "pickup_time_1",

        "Spatial":
            "pickup_location_2dsphere",

        "Spatio-temporal":
            "pickup_location_2dsphere_pickup_time_1",

        "Temporal + Attribute":
            "pickup_time_1",

        "Spatial + Attribute":
            "pickup_location_2dsphere",

        "Spatio-temporal + Attribute":
            "pickup_location_2dsphere_pickup_time_1"
    }


    # -----------------------------------------------------
    # Validate Query Type
    # -----------------------------------------------------

    if query_type not in queries:

        raise HTTPException(
            status_code=400,
            detail=f"Query type not supported: {query_type}"
        )


    # -----------------------------------------------------
    # Select Query and Index
    # -----------------------------------------------------

    query = queries[query_type]

    selected_index = indexes[query_type]


    # -----------------------------------------------------
    # MongoDB Explain Command
    # -----------------------------------------------------

    explain_command = {

        "find":
            collection.name,

        "filter":
            query,

        "hint":
            selected_index
    }


    # -----------------------------------------------------
    # Execute Explain
    # -----------------------------------------------------

    start_time = time.perf_counter()


    try:

        explain_result = db.command(
            "explain",
            explain_command,
            verbosity="executionStats"
        )

    except PyMongoError as e:

        raise HTTPException(
            status_code=503,
            detail=f"MongoDB query failed: {e}"
        )


    end_time = time.perf_counter()


    # -----------------------------------------------------
    # Calculate Execution Time
    # -----------------------------------------------------

    # Round trip includes network + explain overhead
    round_trip_time_ms = (
        end_time - start_time
    ) * 1000


    # -----------------------------------------------------
    # Extract MongoDB Statistics
    # -----------------------------------------------------

    execution_stats = (
        explain_result["executionStats"]
    )


    # Server-side query time reported by MongoDB
    execution_time_ms = (
        execution_stats["executionTimeMillis"]
    )


    documents_returned = (
        execution_stats["nReturned"]
    )


    documents_examined = (
        execution_stats["totalDocsExamined"]
    )


    keys_examined = (
        execution_stats["totalKeysExamined"]
    )


    # -----------------------------------------------------
    # Return Results
    # -----------------------------------------------------

    return {

        "status":
            "ok",

        "query_type":
            query_type,

        "recommended_index":
            selected_index,

        "execution_time_ms":
            execution_time_ms,

        "round_trip_time_ms":
            round(
                round_trip_time_ms,
                2
            ),

        "documents_returned":
            documents_returned,

        "documents_examined":
            documents_examined,

        "keys_examined":
            keys_examined
    }

# ============================================================
# EXPERIMENTAL ANALYTICS API
# ============================================================

from pathlib import Path
import csv
import re
from collections import defaultdict


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = PROJECT_ROOT / "results"


# ------------------------------------------------------------
# CSV HELPERS
# ------------------------------------------------------------

def normalize_key(value):
    if value is None:
        return ""

    return re.sub(
        r"[^a-z0-9]+",
        "_",
        str(value).strip().lower()
    ).strip("_")


def read_result_csv(filename):
    path = RESULTS_DIR / filename

    if not path.exists():
        return []

    with open(
        path,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        rows = []

        for row in reader:

            cleaned = {}

            for key, value in row.items():
                cleaned[normalize_key(key)] = value

            rows.append(cleaned)

        return rows


def get_value(row, *names):

    for name in names:

        key = normalize_key(name)

        if key in row:
            value = row[key]

            if value not in (None, ""):
                return value

    return None


def to_float(value, default=0.0):

    try:
        return float(value)

    except (TypeError, ValueError):
        return default


def to_int(value, default=0):

    try:
        return int(float(value))

    except (TypeError, ValueError):
        return default


# ------------------------------------------------------------
# QUERY TYPE FORMAT
# ------------------------------------------------------------

def pretty_query_type(value):

    if not value:
        return "Unknown"

    mapping = {

        "temporal":
            "Temporal",

        "spatial":
            "Spatial",

        "spatio_temporal":
            "Spatio-temporal",

        "spatiotemporal":
            "Spatio-temporal",

        "temporal_attribute":
            "Temporal + Attribute",

        "spatial_attribute":
            "Spatial + Attribute",

        "spatio_temporal_attribute":
            "Spatio-temporal + Attribute",

        "spatiotemporal_attribute":
            "Spatio-temporal + Attribute",
    }

    normalized = normalize_key(value)

    return mapping.get(
        normalized,
        str(value)
    )


# ------------------------------------------------------------
# LOAD THE ACTUAL EXPERIMENTAL DATA
# ------------------------------------------------------------

def load_experimental_rows():

    rows = read_result_csv(
        "experimental_summary.csv"
    )

    return rows


# ------------------------------------------------------------
# BUILD QUERY TYPE PERFORMANCE
# ------------------------------------------------------------

def build_query_type_summary(rows):

    grouped = defaultdict(list)

    for row in rows:

        query_type = pretty_query_type(
            get_value(
                row,
                "query_type"
            )
        )

        grouped[query_type].append(row)


    result = []


    # Keep the same logical ordering
    # used in the project.

    order = [
        "Spatial",
        "Spatial + Attribute",
        "Spatio-temporal",
        "Spatio-temporal + Attribute",
        "Temporal",
        "Temporal + Attribute"
    ]


    for query_type in order:

        if query_type not in grouped:
            continue

        items = grouped[query_type]

        count = len(items)


        native_values = [
            to_float(
                get_value(
                    row,
                    "native_mean_time_ms"
                )
            )
            for row in items
        ]


        router_values = [
            to_float(
                get_value(
                    row,
                    "router_mean_time_ms"
                )
            )
            for row in items
        ]


        best_values = [
            to_float(
                get_value(
                    row,
                    "best_mean_time_ms"
                )
            )
            for row in items
        ]


        improvement_values = [
            to_float(
                get_value(
                    row,
                    "router_improvement_percent"
                )
            )
            for row in items
        ]


        accuracy_values = []

        for row in items:

            value = get_value(
                row,
                "router_selected_best"
            )

            if value is not None:

                is_correct = (
                    str(value).strip().lower()
                    == "true"
                )

                accuracy_values.append(
                    100 if is_correct else 0
                )


        result.append({

            "query_type":
                query_type,

            "count":
                count,

            "native_ms":
                round(
                    sum(native_values) / count,
                    2
                ),

            "router_ms":
                round(
                    sum(router_values) / count,
                    2
                ),

            "best_ms":
                round(
                    sum(best_values) / count,
                    2
                ),

            "accuracy":
                round(
                    sum(accuracy_values)
                    / len(accuracy_values)
                    if accuracy_values
                    else 0,
                    2
                ),

            "improvement":
                round(
                    sum(improvement_values)
                    / count,
                    2
                )
        })


    return result


# ------------------------------------------------------------
# BUILD ROUTING INFORMATION
# ------------------------------------------------------------

def build_routing_data(rows):

    selected_counts = defaultdict(int)

    best_counts = defaultdict(int)

    total = 0

    correct = 0


    accuracy_groups = defaultdict(
        lambda: {
            "correct": 0,
            "total": 0
        }
    )


    for row in rows:

        selected = get_value(
            row,
            "selected_index"
        )

        best = get_value(
            row,
            "best_index"
        )

        query_type = pretty_query_type(
            get_value(
                row,
                "query_type"
            )
        )


        if selected:

            selected_counts[selected] += 1


        if best:

            best_counts[best] += 1


        router_best = get_value(
            row,
            "router_selected_best"
        )


        if router_best is not None:

            total += 1

            is_correct = (
                str(router_best)
                .strip()
                .lower()
                == "true"
            )


            if is_correct:
                correct += 1


            accuracy_groups[
                query_type
            ]["total"] += 1


            if is_correct:

                accuracy_groups[
                    query_type
                ]["correct"] += 1


    routing_distribution = [

        {
            "index": index,
            "count": count
        }

        for index, count
        in selected_counts.items()
    ]


    best_distribution = [

        {
            "index": index,
            "count": count
        }

        for index, count
        in best_counts.items()
    ]


    accuracy_by_type = []


    order = [
        "Spatial",
        "Spatial + Attribute",
        "Spatio-temporal",
        "Spatio-temporal + Attribute",
        "Temporal",
        "Temporal + Attribute"
    ]


    for query_type in order:

        if query_type not in accuracy_groups:
            continue

        values = accuracy_groups[
            query_type
        ]

        accuracy = (

            values["correct"]
            / values["total"]
            * 100

            if values["total"] > 0

            else 0
        )


        accuracy_by_type.append({

            "query_type":
                query_type,

            "accuracy":
                round(accuracy, 2),

            "correct":
                values["correct"],

            "total":
                values["total"]
        })


    return {

        "total":
            total,

        "correct":
            correct,

        "accuracy":
            round(
                correct / total * 100,
                2
            )
            if total > 0
            else 0,

        "routing_distribution":
            routing_distribution,

        "best_distribution":
            best_distribution,

        "accuracy_by_type":
            accuracy_by_type
    }


# ------------------------------------------------------------
# EXPERIMENTAL SUMMARY
# ------------------------------------------------------------

def build_experimental_summary(rows):

    if not rows:

        return {

            "total_queries": 0,

            "candidate_indexes": 3,

            "router_accuracy": 0,

            "native_avg_ms": 0,

            "router_avg_ms": 0,

            "best_avg_ms": 0,

            "router_improvement": 0,

            "best_improvement": 0,

            "router_gap_from_best": 0,

            "docs_examined_reduction": 0,

            "keys_examined_reduction": 0
        }


    total = len(rows)


    native_values = [

        to_float(
            get_value(
                row,
                "native_mean_time_ms"
            )
        )

        for row in rows
    ]


    router_values = [

        to_float(
            get_value(
                row,
                "router_mean_time_ms"
            )
        )

        for row in rows
    ]


    best_values = [

        to_float(
            get_value(
                row,
                "best_mean_time_ms"
            )
        )

        for row in rows
    ]


    router_improvements = [

        to_float(
            get_value(
                row,
                "router_improvement_percent"
            )
        )

        for row in rows
    ]


    best_improvements = [

        to_float(
            get_value(
                row,
                "best_improvement_percent"
            )
        )

        for row in rows
    ]


    docs_reduction = [

        to_float(
            get_value(
                row,
                "documents_reduction_percent"
            )
        )

        for row in rows
    ]


    keys_reduction = [

        to_float(
            get_value(
                row,
                "keys_reduction_percent"
            )
        )

        for row in rows
    ]


    correct = 0

    for row in rows:

        value = get_value(
            row,
            "router_selected_best"
        )

        if (
            value is not None
            and
            str(value).strip().lower()
            == "true"
        ):

            correct += 1


    native_avg = (
        sum(native_values) / total
    )

    router_avg = (
        sum(router_values) / total
    )

    best_avg = (
        sum(best_values) / total
    )


    router_improvement = (

        (native_avg - router_avg)
        / native_avg
        * 100
    )


    best_improvement = (

        sum(best_improvements)
        / total
    )


    router_gap = (

        (router_avg - best_avg)
        / best_avg
        * 100

        if best_avg > 0

        else 0
    )


    return {

        "total_queries":
            total,

        "candidate_indexes":
            3,

        "router_accuracy":
            round(
                correct / total * 100,
                2
            ),

        "native_avg_ms":
            round(
                native_avg,
                2
            ),

        "router_avg_ms":
            round(
                router_avg,
                2
            ),

        "best_avg_ms":
            round(
                best_avg,
                2
            ),

        "router_improvement":
            round(
                router_improvement,
                2
            ),

        "best_improvement":
            round(
                best_improvement,
                2
            ),

        "router_gap_from_best":
            round(
                router_gap,
                2
            ),

        "docs_examined_reduction":
            round(
                sum(docs_reduction)
                / total,
                2
            ),

        "keys_examined_reduction":
            round(
                sum(keys_reduction)
                / total,
                2
            )
    }


# ------------------------------------------------------------
# MAIN ANALYTICS ENDPOINT
# ------------------------------------------------------------

@app.get("/api/analytics")
def get_analytics():

    rows = load_experimental_rows()


    summary = build_experimental_summary(
        rows
    )


    query_types = build_query_type_summary(
        rows
    )


    routing = build_routing_data(
        rows
    )


    return {

        "status":
            "ok",

        "summary":
            summary,

        "query_types":
            query_types,

        "routing":
            routing
    }