# generate_queries.py

queries = [

    # Q1 - Temporal query
    {
        "query_id": "Q1",
        "query_type": "temporal",
        "description": "Find trips between 10:00 AM and 11:00 AM",
        "filters": {
            "pickup_time": {
                "$gte": "2026-01-01T10:00:00Z",
                "$lt": "2026-01-01T11:00:00Z"
            }
        }
    },

    # Q2 - Spatial query
    {
        "query_id": "Q2",
        "query_type": "spatial",
        "description": "Find trips within approximately 1 km of a location",
        "filters": {
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

    # Q3 - Spatio-temporal query
    {
        "query_id": "Q3",
        "query_type": "spatio_temporal",
        "description": "Find trips within a location and time interval",
        "filters": {
            "pickup_time": {
                "$gte": "2026-01-01T10:00:00Z",
                "$lt": "2026-01-01T11:00:00Z"
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

    # Q4 - Temporal + Attribute query
    {
        "query_id": "Q4",
        "query_type": "temporal_attribute",
        "description": "Find trips between 10:00 AM and 11:00 AM with at least 2 passengers",
        "filters": {
            "pickup_time": {
                "$gte": "2026-01-01T10:00:00Z",
                "$lt": "2026-01-01T11:00:00Z"
            },
            "passenger_count": {
                "$gte": 2
            }
        }
    },

    # Q5 - Spatial + Attribute query
    {
        "query_id": "Q5",
        "query_type": "spatial_attribute",
        "description": "Find trips near the selected location with distance greater than 2 km",
        "filters": {
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

    # Q6 - Spatial + Temporal + Attribute query
    {
        "query_id": "Q6",
        "query_type": "spatio_temporal_attribute",
        "description": "Find trips in the selected location and time interval with at least 2 passengers",
        "filters": {
            "pickup_time": {
                "$gte": "2026-01-01T10:00:00Z",
                "$lt": "2026-01-01T11:00:00Z"
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


if __name__ == "__main__":

    print("Query Workload")
    print("=" * 60)

    for query in queries:
        print(f"\nQuery ID   : {query['query_id']}")
        print(f"Query Type : {query['query_type']}")
        print(f"Description: {query['description']}")