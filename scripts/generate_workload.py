from datetime import datetime


# --------------------------------------------------
# Expanded Query Workload
# 54 query patterns
# --------------------------------------------------

queries = [

    # ==================================================
    # ORIGINAL TEMPORAL QUERIES
    # ==================================================

    {
        "query_id": "T1",
        "query_type": "temporal",
        "description": "1-hour time range",
        "filter": {
            "pickup_time": {
                "$gte": datetime(2026, 1, 1, 10, 0, 0),
                "$lt": datetime(2026, 1, 1, 11, 0, 0)
            }
        }
    },

    {
        "query_id": "T2",
        "query_type": "temporal",
        "description": "2-hour time range",
        "filter": {
            "pickup_time": {
                "$gte": datetime(2026, 1, 1, 10, 0, 0),
                "$lt": datetime(2026, 1, 1, 12, 0, 0)
            }
        }
    },

    {
        "query_id": "T3",
        "query_type": "temporal",
        "description": "30-minute time range",
        "filter": {
            "pickup_time": {
                "$gte": datetime(2026, 1, 1, 10, 0, 0),
                "$lt": datetime(2026, 1, 1, 10, 30, 0)
            }
        }
    },

    # ==================================================
    # ADDITIONAL TEMPORAL QUERIES
    # ==================================================

    {
        "query_id": "T4",
        "query_type": "temporal",
        "description": "15-minute time range",
        "filter": {
            "pickup_time": {
                "$gte": datetime(2026, 1, 1, 10, 0, 0),
                "$lt": datetime(2026, 1, 1, 10, 15, 0)
            }
        }
    },

    {
        "query_id": "T5",
        "query_type": "temporal",
        "description": "3-hour time range",
        "filter": {
            "pickup_time": {
                "$gte": datetime(2026, 1, 1, 10, 0, 0),
                "$lt": datetime(2026, 1, 1, 13, 0, 0)
            }
        }
    },

    {
        "query_id": "T6",
        "query_type": "temporal",
        "description": "6-hour time range",
        "filter": {
            "pickup_time": {
                "$gte": datetime(2026, 1, 1, 8, 0, 0),
                "$lt": datetime(2026, 1, 1, 14, 0, 0)
            }
        }
    },

    {
        "query_id": "T7",
        "query_type": "temporal",
        "description": "30-minute afternoon range",
        "filter": {
            "pickup_time": {
                "$gte": datetime(2026, 1, 1, 14, 0, 0),
                "$lt": datetime(2026, 1, 1, 14, 30, 0)
            }
        }
    },

    {
        "query_id": "T8",
        "query_type": "temporal",
        "description": "2-hour afternoon range",
        "filter": {
            "pickup_time": {
                "$gte": datetime(2026, 1, 1, 14, 0, 0),
                "$lt": datetime(2026, 1, 1, 16, 0, 0)
            }
        }
    },

    {
        "query_id": "T9",
        "query_type": "temporal",
        "description": "1-hour evening range",
        "filter": {
            "pickup_time": {
                "$gte": datetime(2026, 1, 1, 18, 0, 0),
                "$lt": datetime(2026, 1, 1, 19, 0, 0)
            }
        }
    },


    # ==================================================
    # ORIGINAL SPATIAL QUERIES
    # ==================================================

    {
        "query_id": "S1",
        "query_type": "spatial",
        "description": "0.5 km radius",
        "filter": {
            "pickup_location": {
                "$geoWithin": {
                    "$centerSphere": [
                        [-73.9857, 40.7484],
                        0.5 / 6378.1
                    ]
                }
            }
        }
    },

    {
        "query_id": "S2",
        "query_type": "spatial",
        "description": "1 km radius",
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

    {
        "query_id": "S3",
        "query_type": "spatial",
        "description": "2 km radius",
        "filter": {
            "pickup_location": {
                "$geoWithin": {
                    "$centerSphere": [
                        [-73.9857, 40.7484],
                        2 / 6378.1
                    ]
                }
            }
        }
    },

    # ==================================================
    # ADDITIONAL SPATIAL QUERIES
    # ==================================================

    {
        "query_id": "S4",
        "query_type": "spatial",
        "description": "0.25 km radius",
        "filter": {
            "pickup_location": {
                "$geoWithin": {
                    "$centerSphere": [
                        [-73.9857, 40.7484],
                        0.25 / 6378.1
                    ]
                }
            }
        }
    },

    {
        "query_id": "S5",
        "query_type": "spatial",
        "description": "1.5 km radius",
        "filter": {
            "pickup_location": {
                "$geoWithin": {
                    "$centerSphere": [
                        [-73.9857, 40.7484],
                        1.5 / 6378.1
                    ]
                }
            }
        }
    },

    {
        "query_id": "S6",
        "query_type": "spatial",
        "description": "3 km radius",
        "filter": {
            "pickup_location": {
                "$geoWithin": {
                    "$centerSphere": [
                        [-73.9857, 40.7484],
                        3 / 6378.1
                    ]
                }
            }
        }
    },

    {
        "query_id": "S7",
        "query_type": "spatial",
        "description": "0.5 km around Times Square",
        "filter": {
            "pickup_location": {
                "$geoWithin": {
                    "$centerSphere": [
                        [-73.9851, 40.7580],
                        0.5 / 6378.1
                    ]
                }
            }
        }
    },

    {
        "query_id": "S8",
        "query_type": "spatial",
        "description": "1 km around Times Square",
        "filter": {
            "pickup_location": {
                "$geoWithin": {
                    "$centerSphere": [
                        [-73.9851, 40.7580],
                        1 / 6378.1
                    ]
                }
            }
        }
    },

    {
        "query_id": "S9",
        "query_type": "spatial",
        "description": "2 km around Times Square",
        "filter": {
            "pickup_location": {
                "$geoWithin": {
                    "$centerSphere": [
                        [-73.9851, 40.7580],
                        2 / 6378.1
                    ]
                }
            }
        }
    },


    # ==================================================
    # ORIGINAL SPATIO-TEMPORAL QUERIES
    # ==================================================

    {
        "query_id": "ST1",
        "query_type": "spatio_temporal",
        "description": "1-hour + 0.5 km",
        "filter": {
            "pickup_time": {
                "$gte": datetime(2026, 1, 1, 10, 0, 0),
                "$lt": datetime(2026, 1, 1, 11, 0, 0)
            },
            "pickup_location": {
                "$geoWithin": {
                    "$centerSphere": [
                        [-73.9857, 40.7484],
                        0.5 / 6378.1
                    ]
                }
            }
        }
    },

    {
        "query_id": "ST2",
        "query_type": "spatio_temporal",
        "description": "1-hour + 1 km",
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

    {
        "query_id": "ST3",
        "query_type": "spatio_temporal",
        "description": "2-hour + 2 km",
        "filter": {
            "pickup_time": {
                "$gte": datetime(2026, 1, 1, 10, 0, 0),
                "$lt": datetime(2026, 1, 1, 12, 0, 0)
            },
            "pickup_location": {
                "$geoWithin": {
                    "$centerSphere": [
                        [-73.9857, 40.7484],
                        2 / 6378.1
                    ]
                }
            }
        }
    },

    # ==================================================
    # ADDITIONAL SPATIO-TEMPORAL QUERIES
    # ==================================================

    {
        "query_id": "ST4",
        "query_type": "spatio_temporal",
        "description": "30-minute + 0.25 km",
        "filter": {
            "pickup_time": {
                "$gte": datetime(2026, 1, 1, 10, 0, 0),
                "$lt": datetime(2026, 1, 1, 10, 30, 0)
            },
            "pickup_location": {
                "$geoWithin": {
                    "$centerSphere": [
                        [-73.9857, 40.7484],
                        0.25 / 6378.1
                    ]
                }
            }
        }
    },

    {
        "query_id": "ST5",
        "query_type": "spatio_temporal",
        "description": "30-minute + 1 km",
        "filter": {
            "pickup_time": {
                "$gte": datetime(2026, 1, 1, 10, 0, 0),
                "$lt": datetime(2026, 1, 1, 10, 30, 0)
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

    {
        "query_id": "ST6",
        "query_type": "spatio_temporal",
        "description": "3-hour + 1.5 km",
        "filter": {
            "pickup_time": {
                "$gte": datetime(2026, 1, 1, 10, 0, 0),
                "$lt": datetime(2026, 1, 1, 13, 0, 0)
            },
            "pickup_location": {
                "$geoWithin": {
                    "$centerSphere": [
                        [-73.9857, 40.7484],
                        1.5 / 6378.1
                    ]
                }
            }
        }
    },

    {
        "query_id": "ST7",
        "query_type": "spatio_temporal",
        "description": "1-hour + 2 km at Times Square",
        "filter": {
            "pickup_time": {
                "$gte": datetime(2026, 1, 1, 10, 0, 0),
                "$lt": datetime(2026, 1, 1, 11, 0, 0)
            },
            "pickup_location": {
                "$geoWithin": {
                    "$centerSphere": [
                        [-73.9851, 40.7580],
                        2 / 6378.1
                    ]
                }
            }
        }
    },

    {
        "query_id": "ST8",
        "query_type": "spatio_temporal",
        "description": "2-hour + 0.5 km at Times Square",
        "filter": {
            "pickup_time": {
                "$gte": datetime(2026, 1, 1, 10, 0, 0),
                "$lt": datetime(2026, 1, 1, 12, 0, 0)
            },
            "pickup_location": {
                "$geoWithin": {
                    "$centerSphere": [
                        [-73.9851, 40.7580],
                        0.5 / 6378.1
                    ]
                }
            }
        }
    },

    {
        "query_id": "ST9",
        "query_type": "spatio_temporal",
        "description": "6-hour + 3 km",
        "filter": {
            "pickup_time": {
                "$gte": datetime(2026, 1, 1, 8, 0, 0),
                "$lt": datetime(2026, 1, 1, 14, 0, 0)
            },
            "pickup_location": {
                "$geoWithin": {
                    "$centerSphere": [
                        [-73.9857, 40.7484],
                        3 / 6378.1
                    ]
                }
            }
        }
    },


    # ==================================================
    # ORIGINAL TEMPORAL + ATTRIBUTE
    # ==================================================

    {
        "query_id": "TA1",
        "query_type": "temporal_attribute",
        "description": "1-hour + passenger >= 2",
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

    {
        "query_id": "TA2",
        "query_type": "temporal_attribute",
        "description": "1-hour + passenger >= 4",
        "filter": {
            "pickup_time": {
                "$gte": datetime(2026, 1, 1, 10, 0, 0),
                "$lt": datetime(2026, 1, 1, 11, 0, 0)
            },
            "passenger_count": {
                "$gte": 4
            }
        }
    },

    {
        "query_id": "TA3",
        "query_type": "temporal_attribute",
        "description": "2-hour + passenger >= 2",
        "filter": {
            "pickup_time": {
                "$gte": datetime(2026, 1, 1, 10, 0, 0),
                "$lt": datetime(2026, 1, 1, 12, 0, 0)
            },
            "passenger_count": {
                "$gte": 2
            }
        }
    },

    # ==================================================
    # ADDITIONAL TEMPORAL + ATTRIBUTE
    # ==================================================

    {
        "query_id": "TA4",
        "query_type": "temporal_attribute",
        "description": "30-minute + passenger >= 2",
        "filter": {
            "pickup_time": {
                "$gte": datetime(2026, 1, 1, 10, 0, 0),
                "$lt": datetime(2026, 1, 1, 10, 30, 0)
            },
            "passenger_count": {
                "$gte": 2
            }
        }
    },

    {
        "query_id": "TA5",
        "query_type": "temporal_attribute",
        "description": "2-hour + passenger >= 4",
        "filter": {
            "pickup_time": {
                "$gte": datetime(2026, 1, 1, 10, 0, 0),
                "$lt": datetime(2026, 1, 1, 12, 0, 0)
            },
            "passenger_count": {
                "$gte": 4
            }
        }
    },

    {
        "query_id": "TA6",
        "query_type": "temporal_attribute",
        "description": "3-hour + passenger >= 2",
        "filter": {
            "pickup_time": {
                "$gte": datetime(2026, 1, 1, 10, 0, 0),
                "$lt": datetime(2026, 1, 1, 13, 0, 0)
            },
            "passenger_count": {
                "$gte": 2
            }
        }
    },

    {
        "query_id": "TA7",
        "query_type": "temporal_attribute",
        "description": "1-hour + passenger >= 5",
        "filter": {
            "pickup_time": {
                "$gte": datetime(2026, 1, 1, 10, 0, 0),
                "$lt": datetime(2026, 1, 1, 11, 0, 0)
            },
            "passenger_count": {
                "$gte": 5
            }
        }
    },

    {
        "query_id": "TA8",
        "query_type": "temporal_attribute",
        "description": "6-hour + passenger >= 4",
        "filter": {
            "pickup_time": {
                "$gte": datetime(2026, 1, 1, 8, 0, 0),
                "$lt": datetime(2026, 1, 1, 14, 0, 0)
            },
            "passenger_count": {
                "$gte": 4
            }
        }
    },

    {
        "query_id": "TA9",
        "query_type": "temporal_attribute",
        "description": "1-hour + passenger >= 1",
        "filter": {
            "pickup_time": {
                "$gte": datetime(2026, 1, 1, 18, 0, 0),
                "$lt": datetime(2026, 1, 1, 19, 0, 0)
            },
            "passenger_count": {
                "$gte": 1
            }
        }
    },


    # ==================================================
    # ORIGINAL SPATIAL + ATTRIBUTE
    # ==================================================

    {
        "query_id": "SA1",
        "query_type": "spatial_attribute",
        "description": "0.5 km + distance > 2",
        "filter": {
            "pickup_location": {
                "$geoWithin": {
                    "$centerSphere": [
                        [-73.9857, 40.7484],
                        0.5 / 6378.1
                    ]
                }
            },
            "trip_distance": {
                "$gt": 2
            }
        }
    },

    {
        "query_id": "SA2",
        "query_type": "spatial_attribute",
        "description": "1 km + distance > 5",
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
                "$gt": 5
            }
        }
    },

    {
        "query_id": "SA3",
        "query_type": "spatial_attribute",
        "description": "2 km + distance > 2",
        "filter": {
            "pickup_location": {
                "$geoWithin": {
                    "$centerSphere": [
                        [-73.9857, 40.7484],
                        2 / 6378.1
                    ]
                }
            },
            "trip_distance": {
                "$gt": 2
            }
        }
    },

    # ==================================================
    # ADDITIONAL SPATIAL + ATTRIBUTE
    # ==================================================

    {
        "query_id": "SA4",
        "query_type": "spatial_attribute",
        "description": "0.25 km + distance > 2",
        "filter": {
            "pickup_location": {
                "$geoWithin": {
                    "$centerSphere": [
                        [-73.9857, 40.7484],
                        0.25 / 6378.1
                    ]
                }
            },
            "trip_distance": {
                "$gt": 2
            }
        }
    },

    {
        "query_id": "SA5",
        "query_type": "spatial_attribute",
        "description": "1.5 km + distance > 5",
        "filter": {
            "pickup_location": {
                "$geoWithin": {
                    "$centerSphere": [
                        [-73.9857, 40.7484],
                        1.5 / 6378.1
                    ]
                }
            },
            "trip_distance": {
                "$gt": 5
            }
        }
    },

    {
        "query_id": "SA6",
        "query_type": "spatial_attribute",
        "description": "3 km + distance > 2",
        "filter": {
            "pickup_location": {
                "$geoWithin": {
                    "$centerSphere": [
                        [-73.9857, 40.7484],
                        3 / 6378.1
                    ]
                }
            },
            "trip_distance": {
                "$gt": 2
            }
        }
    },

    {
        "query_id": "SA7",
        "query_type": "spatial_attribute",
        "description": "0.5 km + distance > 5 at Times Square",
        "filter": {
            "pickup_location": {
                "$geoWithin": {
                    "$centerSphere": [
                        [-73.9851, 40.7580],
                        0.5 / 6378.1
                    ]
                }
            },
            "trip_distance": {
                "$gt": 5
            }
        }
    },

    {
        "query_id": "SA8",
        "query_type": "spatial_attribute",
        "description": "1 km + distance > 2 at Times Square",
        "filter": {
            "pickup_location": {
                "$geoWithin": {
                    "$centerSphere": [
                        [-73.9851, 40.7580],
                        1 / 6378.1
                    ]
                }
            },
            "trip_distance": {
                "$gt": 2
            }
        }
    },

    {
        "query_id": "SA9",
        "query_type": "spatial_attribute",
        "description": "2 km + distance > 5 at Times Square",
        "filter": {
            "pickup_location": {
                "$geoWithin": {
                    "$centerSphere": [
                        [-73.9851, 40.7580],
                        2 / 6378.1
                    ]
                }
            },
            "trip_distance": {
                "$gt": 5
            }
        }
    },


    # ==================================================
    # ORIGINAL SPATIO-TEMPORAL + ATTRIBUTE
    # ==================================================

    {
        "query_id": "STA1",
        "query_type": "spatio_temporal_attribute",
        "description": "1-hour + 0.5 km + passenger >= 2",
        "filter": {
            "pickup_time": {
                "$gte": datetime(2026, 1, 1, 10, 0, 0),
                "$lt": datetime(2026, 1, 1, 11, 0, 0)
            },
            "pickup_location": {
                "$geoWithin": {
                    "$centerSphere": [
                        [-73.9857, 40.7484],
                        0.5 / 6378.1
                    ]
                }
            },
            "passenger_count": {
                "$gte": 2
            }
        }
    },

    {
        "query_id": "STA2",
        "query_type": "spatio_temporal_attribute",
        "description": "1-hour + 1 km + passenger >= 4",
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
                "$gte": 4
            }
        }
    },

    {
        "query_id": "STA3",
        "query_type": "spatio_temporal_attribute",
        "description": "2-hour + 2 km + passenger >= 2",
        "filter": {
            "pickup_time": {
                "$gte": datetime(2026, 1, 1, 10, 0, 0),
                "$lt": datetime(2026, 1, 1, 12, 0, 0)
            },
            "pickup_location": {
                "$geoWithin": {
                    "$centerSphere": [
                        [-73.9857, 40.7484],
                        2 / 6378.1
                    ]
                }
            },
            "passenger_count": {
                "$gte": 2
            }
        }
    },

    # ==================================================
    # ADDITIONAL SPATIO-TEMPORAL + ATTRIBUTE
    # ==================================================

    {
        "query_id": "STA4",
        "query_type": "spatio_temporal_attribute",
        "description": "30-minute + 0.25 km + passenger >= 2",
        "filter": {
            "pickup_time": {
                "$gte": datetime(2026, 1, 1, 10, 0, 0),
                "$lt": datetime(2026, 1, 1, 10, 30, 0)
            },
            "pickup_location": {
                "$geoWithin": {
                    "$centerSphere": [
                        [-73.9857, 40.7484],
                        0.25 / 6378.1
                    ]
                }
            },
            "passenger_count": {
                "$gte": 2
            }
        }
    },

    {
        "query_id": "STA5",
        "query_type": "spatio_temporal_attribute",
        "description": "30-minute + 1 km + passenger >= 4",
        "filter": {
            "pickup_time": {
                "$gte": datetime(2026, 1, 1, 10, 0, 0),
                "$lt": datetime(2026, 1, 1, 10, 30, 0)
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
                "$gte": 4
            }
        }
    },

    {
        "query_id": "STA6",
        "query_type": "spatio_temporal_attribute",
        "description": "3-hour + 1.5 km + passenger >= 2",
        "filter": {
            "pickup_time": {
                "$gte": datetime(2026, 1, 1, 10, 0, 0),
                "$lt": datetime(2026, 1, 1, 13, 0, 0)
            },
            "pickup_location": {
                "$geoWithin": {
                    "$centerSphere": [
                        [-73.9857, 40.7484],
                        1.5 / 6378.1
                    ]
                }
            },
            "passenger_count": {
                "$gte": 2
            }
        }
    },

    {
        "query_id": "STA7",
        "query_type": "spatio_temporal_attribute",
        "description": "1-hour + 2 km + passenger >= 5",
        "filter": {
            "pickup_time": {
                "$gte": datetime(2026, 1, 1, 14, 0, 0),
                "$lt": datetime(2026, 1, 1, 15, 0, 0)
            },
            "pickup_location": {
                "$geoWithin": {
                    "$centerSphere": [
                        [-73.9851, 40.7580],
                        2 / 6378.1
                    ]
                }
            },
            "passenger_count": {
                "$gte": 5
            }
        }
    },

    {
        "query_id": "STA8",
        "query_type": "spatio_temporal_attribute",
        "description": "2-hour + 0.5 km + passenger >= 4",
        "filter": {
            "pickup_time": {
                "$gte": datetime(2026, 1, 1, 14, 0, 0),
                "$lt": datetime(2026, 1, 1, 16, 0, 0)
            },
            "pickup_location": {
                "$geoWithin": {
                    "$centerSphere": [
                        [-73.9851, 40.7580],
                        0.5 / 6378.1
                    ]
                }
            },
            "passenger_count": {
                "$gte": 4
            }
        }
    },

    {
        "query_id": "STA9",
        "query_type": "spatio_temporal_attribute",
        "description": "6-hour + 3 km + passenger >= 2",
        "filter": {
            "pickup_time": {
                "$gte": datetime(2026, 1, 1, 8, 0, 0),
                "$lt": datetime(2026, 1, 1, 14, 0, 0)
            },
            "pickup_location": {
                "$geoWithin": {
                    "$centerSphere": [
                        [-73.9857, 40.7484],
                        3 / 6378.1
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
# Display workload
# --------------------------------------------------

print("=" * 70)
print("EXPANDED QUERY WORKLOAD")
print("=" * 70)

print("Total queries:", len(queries))

for query in queries:

    print(
        f"{query['query_id']:5s} | "
        f"{query['query_type']:25s} | "
        f"{query['description']}"
    )

print("=" * 70)