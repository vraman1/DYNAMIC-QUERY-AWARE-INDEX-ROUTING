import pandas as pd

# Load cleaned dataset
file_path = "data/cleaned_taxi_data_full.parquet"

df = pd.read_parquet(file_path)

print("\n========================================")
print("CLEANED DATASET VERIFICATION")
print("========================================")

print("\nNumber of records:", len(df))
print("Number of columns:", len(df.columns))

print("\nColumns:")
for column in df.columns:
    print("-", column)

print("\n----------------------------------------")
print("Missing values")
print("----------------------------------------")

print(df.isnull().sum())

print("\n----------------------------------------")
print("Data types")
print("----------------------------------------")

print(df.dtypes)

print("\n----------------------------------------")
print("Coordinate ranges")
print("----------------------------------------")

print("Pickup longitude:",
      df["pickup_longitude"].min(),
      "to",
      df["pickup_longitude"].max())

print("Pickup latitude:",
      df["pickup_latitude"].min(),
      "to",
      df["pickup_latitude"].max())

print("Dropoff longitude:",
      df["dropoff_longitude"].min(),
      "to",
      df["dropoff_longitude"].max())

print("Dropoff latitude:",
      df["dropoff_latitude"].min(),
      "to",
      df["dropoff_latitude"].max())

print("\n----------------------------------------")
print("Sample records")
print("----------------------------------------")

print(df.head(5).to_string(index=False))