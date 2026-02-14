import pandas as pd
from sqlalchemy import create_engine
from config import DATABASE_URL
import os

# ---------------------------
# LOAD DATA
# ---------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

trips_path = os.path.join(BASE_DIR, "dataset", "yellow_tripdata_2019-01.csv")
zones_path = os.path.join(BASE_DIR, "dataset", "taxi_zone_lookup.csv")

# Parse datetime columns immediately (important fix)
trips = pd.read_csv(
    trips_path,
    parse_dates=["tpep_pickup_datetime", "tpep_dropoff_datetime"]
)

zones = pd.read_csv(zones_path)

# ---------------------------
# DATA CLEANING
# ---------------------------

# Remove negative or zero distances
trips = trips[trips["trip_distance"] > 0]

# Remove negative fares
trips = trips[trips["total_amount"] > 0]

# Remove invalid time records
trips = trips[
    trips["tpep_dropoff_datetime"] > trips["tpep_pickup_datetime"]
]

# Create duration (minutes)
trips["duration_minutes"] = (
    trips["tpep_dropoff_datetime"] - trips["tpep_pickup_datetime"]
).dt.total_seconds() / 60

# Remove extreme durations (> 300 mins)
trips = trips[trips["duration_minutes"] < 300]

# ---------------------------
# FEATURE ENGINEERING
# ---------------------------

# Fare per mile
trips["fare_per_mile"] = trips["total_amount"] / trips["trip_distance"]

# Revenue per minute
trips["revenue_per_min"] = trips["total_amount"] / trips["duration_minutes"]

# Rush hour flag (vectorized – faster than apply)
trips["hour"] = trips["tpep_pickup_datetime"].dt.hour

trips["rush_hour_flag"] = trips["hour"].isin(
    list(range(7, 10)) + list(range(16, 20))
).astype(int)

# ---------------------------
# SELECT FINAL COLUMNS
# ---------------------------

trips = trips[[
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
    "passenger_count",
    "trip_distance",
    "total_amount",
    "duration_minutes",
    "fare_per_mile",
    "revenue_per_min",
    "rush_hour_flag",
    "PULocationID",
    "DOLocationID"
]]

trips.columns = [
    "pickup_datetime",
    "dropoff_datetime",
    "passenger_count",
    "trip_distance",
    "total_amount",
    "duration_minutes",
    "fare_per_mile",
    "revenue_per_min",
    "rush_hour_flag",
    "pickup_zone_id",
    "dropoff_zone_id"
]

# ---------------------------
# INSERT INTO DATABASE
# ---------------------------

engine = create_engine(DATABASE_URL)

zones.columns = ["zone_id", "borough", "zone_name", "service_zone"]

zones.to_sql("zones", engine, if_exists="append", index=False)
trips.to_sql("trips", engine, if_exists="append", index=False, chunksize=10000, method="multi")

print("Data successfully inserted!")
