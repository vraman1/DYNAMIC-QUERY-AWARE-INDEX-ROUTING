import pandas as pd

file_path = "data/yellow_tripdata_2026-01.parquet"

df = pd.read_parquet(file_path)

print("\nDataset loaded successfully!")
print("Number of rows:", len(df))
print("Number of columns:", len(df.columns))

print("\nColumns:")
for column in df.columns:
    print("-", column)

print("\nFirst 5 records:")
print(df.head())