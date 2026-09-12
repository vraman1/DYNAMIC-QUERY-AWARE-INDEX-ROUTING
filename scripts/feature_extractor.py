from datetime import datetime


# --------------------------------------------------
# Query Feature Extractor
# --------------------------------------------------

def extract_features(query_id, query_type, query_filter, result_size):
    """
    Extract features from a MongoDB query.

    Parameters:
        query_id      : Query identifier (Q1, Q2, ...)
        query_type    : Type of query
        query_filter  : MongoDB filter
        result_size   : Number of documents returned

    Returns:
        Dictionary containing query features.
    """

    # --------------------------------------------------
    # Detect query characteristics
    # --------------------------------------------------

    spatial_query = 0
    temporal_query = 0
    attribute_query = 0
    has_2dsphere = 0
    has_time_filter = 0

    number_of_filters = 0


    # --------------------------------------------------
    # Check each query field
    # --------------------------------------------------

    if "pickup_location" in query_filter:

        spatial_query = 1
        has_2dsphere = 1
        number_of_filters += 1


    if "pickup_time" in query_filter:

        temporal_query = 1
        has_time_filter = 1
        number_of_filters += 1


    if "passenger_count" in query_filter:

        attribute_query = 1
        number_of_filters += 1


    if "trip_distance" in query_filter:

        attribute_query = 1
        number_of_filters += 1


    # --------------------------------------------------
    # Calculate query selectivity
    # --------------------------------------------------

    total_documents = 495160

    query_selectivity = result_size / total_documents


    # --------------------------------------------------
    # Create feature dictionary
    # --------------------------------------------------

    features = {

        "query_id": query_id,

        "query_type": query_type,

        "spatial_query": spatial_query,

        "temporal_query": temporal_query,

        "attribute_query": attribute_query,

        "has_2dsphere": has_2dsphere,

        "has_time_filter": has_time_filter,

        "number_of_filters": number_of_filters,

        "result_size": result_size,

        "query_selectivity": query_selectivity
    }


    return features


# --------------------------------------------------
# Test the extractor
# --------------------------------------------------

if __name__ == "__main__":

    # Example Q3 query

    example_query = {

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


    # Q3 returned 215 documents
    features = extract_features(
        "Q3",
        "spatio_temporal",
        example_query,
        215
    )


    # --------------------------------------------------
    # Display extracted features
    # --------------------------------------------------

    print("=" * 70)
    print("QUERY FEATURE EXTRACTION")
    print("=" * 70)

    for feature, value in features.items():

        print(
            f"{feature:25s}: {value}"
        )

    print("=" * 70)