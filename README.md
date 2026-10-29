# Dynamic Query-Aware Index Routing for Spatio-Temporal Data in Document-Oriented NoSQL Systems

## Overview
This project implements a query-aware index routing system for spatio-temporal workloads in MongoDB.

The system analyzes an incoming query, extracts its characteristics, and selects an appropriate MongoDB index from a set of candidate indexes. The selected index is then used to execute the query and measure its performance.

## Project Pipeline
```text
Dataset → Data Preparation → MongoDB → Candidate Indexes → Query Workload
→ Feature Extraction → Index Router → Query Execution → Performance Comparison
```

## Requirements
- Git
- Python 3.10 or later
- MongoDB
- Node.js
- npm

Developed and tested with:
- Python 3.10.11
- MongoDB 8.3.7
- Node.js 24.21.0
- npm 11.9.0

# Running the Project Locally

## 1. Clone the Repository
Open PowerShell and navigate to where you want the project:

```powershell
cd E:\GitHub
```

Clone the repository:

```powershell
git clone https://github.com/vraman1/DYNAMIC-QUERY-AWARE-INDEX-ROUTING
```

Enter the project directory:

```powershell
cd "DYNAMIC QUERY-AWARE INDEX ROUTING"
```

## 2. Set Up Python

Check Python:

```powershell
python --version
```

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 3. Install Python Dependencies

```powershell
pip install -r requirements.txt
```

`geopandas` and `shapely` are only needed for the data-preparation scripts (`prepare_data.py`, `inspect_zones.py`).

## 4. Start MongoDB

Install MongoDB Community Server and start the MongoDB service.

The project expects:

```text
mongodb://localhost:27017/
```

Database:

```text
dqi_project
```

Collection:

```text
spatiotemporal_data
```

Verify with:

```powershell
mongosh
```

## 5. Load the Dataset

The repository contains:

```text
data/cleaned_taxi_data.parquet
```

The experiment uses 495,160 valid records.

The large raw/full datasets are intentionally excluded from GitHub:

```text
cleaned_taxi_data_full.parquet
yellow_tripdata_2026-01.parquet
```

With MongoDB running, execute:

```powershell
python scripts/load_data.py
```

Verify:

```powershell
mongosh
```

```javascript
use dqi_project
db.spatiotemporal_data.countDocuments()
```

Expected:

```text
495160
```

> Run `load_data.py` only once. It does not clear the collection, so running it again inserts duplicate documents.

## 6. Create MongoDB Indexes

The backend forces one of three candidate indexes for every query, so these must exist or Execute Query fails.

With MongoDB running, execute:

```powershell
python scripts/create_indexes.py
```

The script is safe to run more than once; existing indexes are skipped.

Alternatively, create them manually in `mongosh`:

### Temporal Index

```javascript
db.spatiotemporal_data.createIndex({
    pickup_time: 1
})
```

### Spatial Index

```javascript
db.spatiotemporal_data.createIndex({
    pickup_location: "2dsphere"
})
```

### Compound Spatial-Temporal Index

```javascript
db.spatiotemporal_data.createIndex({
    pickup_location: "2dsphere",
    pickup_time: 1
})
```

Verify:

```javascript
db.spatiotemporal_data.getIndexes()
```

## 7. Install Frontend Dependencies

Open another terminal:

```powershell
cd "E:\GitHub\DYNAMIC QUERY-AWARE INDEX ROUTING\frontend"
npm install
```

`node_modules` is excluded from GitHub and is recreated using `npm install`.

## 8. Start the Backend

Open a terminal:

```powershell
cd "E:\GitHub\DYNAMIC QUERY-AWARE INDEX ROUTING\backend"
..\.venv\Scripts\Activate.ps1
python -m uvicorn main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

Keep this terminal running.

## 9. Start the Frontend

Open a second terminal:

```powershell
cd "E:\GitHub\DYNAMIC QUERY-AWARE INDEX ROUTING\frontend"
npm run dev
```

Open the URL displayed by Vite, normally:

```text
http://localhost:5173
```

or:

```text
http://localhost:5174
```

# Complete Local Setup

```text
MongoDB running
     ↓
Load data and create indexes
     ↓
FastAPI backend running on port 8000
     ↓
React/Vite frontend running on port 5173/5174
     ↓
Open dashboard in browser
```

# Project Structure

```text
DYNAMIC QUERY-AWARE INDEX ROUTING
├── backend/
├── data/
├── frontend/
├── results/
├── scripts/
├── .gitignore
└── README.md
```

# Experimental Workload

The expanded workload contains 54 queries:

| Query Type | Number |
|---|---:|
| Temporal | 9 |
| Spatial | 9 |
| Spatio-temporal | 9 |
| Temporal + Attribute | 9 |
| Spatial + Attribute | 9 |
| Spatio-temporal + Attribute | 9 |
| **Total** | **54** |

Candidate benchmark:

```text
54 queries × 3 candidate indexes × 5 runs = 810 executions
```

## Rule-Based Router

The router uses:
- Spatial query
- Temporal query
- Attribute query

Example:

```text
Temporal → pickup_time_1
Spatial → pickup_location_2dsphere
Spatial + Temporal → pickup_location_2dsphere_pickup_time_1
```

## Machine Learning Router

Decision Tree configuration:

```text
Algorithm: DecisionTreeClassifier
Maximum Depth: 4
Random State: 42
Validation: Leave-One-Out Cross-Validation
```

Results:

```text
Training Accuracy: 96.30%
LOOCV Accuracy: 88.89%
Correct Predictions: 52 / 54
```

# Experimental Results

Rule-based router:

```text
51 / 54 best-index selections
94.44% routing accuracy
```

Average execution time:

| Approach | Average Execution Time |
|---|---:|
| Native MongoDB | 718.63 ms |
| Rule-Based Router | 661.89 ms |
| Empirical Best Index | 686.53 ms |

The rule-based router showed an average execution-time reduction of approximately **7.90%** compared with the native MongoDB benchmark in this experiment.

These are measured experimental results and can vary with hardware, database state, and system load.

# Limitations

1. The experiment uses a subset of the full January 2026 TLC dataset.
2. The workload contains 54 designed queries rather than a production query log.
3. Query execution times can vary with system and database state.
4. The routing policy is currently rule-based.
5. Three primary candidate indexes are evaluated.
6. Spatial coordinates are based on taxi-zone centroids rather than raw GPS traces.
7. Results depend on MongoDB configuration, hardware, dataset, and workload.

# Important Scripts

```text
inspect_dataset.py
prepare_data.py
verify_data.py
load_data.py
create_indexes.py
generate_queries.py
benchmark.py
repeat_benchmark.py
feature_extractor.py
generate_features.py
rule_router.py
router_benchmark.py
compare_results.py
generate_workload.py
candidate_index_benchmark.py
analyze_candidate_benchmark.py
create_experimental_summary.py
prepare_ml_dataset.py
train_ml_router.py
```

Run scripts from the project root:

```powershell
python scripts/<script_name>.py
```

# Technologies Used

- MongoDB
- Python
- FastAPI
- React
- Vite
- JavaScript
- PyMongo
- Pandas
- PyArrow
- Scikit-learn
- Recharts
- NYC TLC Yellow Taxi Dataset

# Future Work

- Larger datasets
- Larger and more diverse query workloads
- Automated workload generation
- Cost-based index selection
- Advanced machine-learning routing models
- Online learning from query execution feedback
- Adaptive index selection
- Index maintenance-cost analysis
- Memory and storage overhead analysis
- Distributed MongoDB deployments

# Academic Project

**Course:** CSE3086 – NoSQL Databases

**Project:** Dynamic Query-Aware Index Routing for Spatio-Temporal Data in Document-Oriented NoSQL Systems
