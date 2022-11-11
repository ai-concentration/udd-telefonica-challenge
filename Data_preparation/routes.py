import pandas as pd

from pathlib import Path

DTYPE = {
    "lat": "string",  # Handling lat as string avoids floating precision errors
    "lon": "string"  # Handling lon as string avoids floating precision errors
}

DATA_DIR = Path("data")  # Define directory for datasets
JSON_DIR = Path("json")  # Define directory for JSONs

# Loading the dataset
print("Loading dataset...")

dataset = pd.read_csv(
    DATA_DIR / "data.csv",
    dtype=DTYPE
)

print("Done!")

import json

from collections import defaultdict
from datetime import datetime  # So we can deal with timestamps strings

# Specify time format by which timestamp strings will be parsed
TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"

# Get first timestamp in dataset and convert it to datetime object
FIRST_TIMESTAMP = datetime.strptime(dataset["timestamp"][0], TIME_FORMAT)


def get_time_dummy(timestamp):
    """
    Convert each timestamp from dataset to time dummy
    """
    timestamp = datetime.strptime(timestamp, TIME_FORMAT)

    seconds_delta = timestamp - FIRST_TIMESTAMP

    return int(seconds_delta.total_seconds())  # Time dummies are computed per second


# Update timestamp column with time dummy values
print("Converting timestamp values to time dummies...")

dataset["timestamp"] = dataset["timestamp"].apply(get_time_dummy)  # apply method performs in parallel

print("Done!")

bts_latlon_mapping = None

print("Loading bts/lat lon mapping...")

with open(JSON_DIR / "bts_latlon_mapping.json", "r") as f:
    bts_latlon_mapping = json.load(f)

print("Done!")


def clean_lat_lon(bts_id):
    lat = bts_latlon_mapping[bts_id].split(",")[0]
    lon = bts_latlon_mapping[bts_id].split(",")[1]

    return lat, lon


# Update lat and lon columns
print("Updating lat and lon columns...")

dataset["lat"], dataset["lon"] = zip(*dataset["bts_id"].apply(clean_lat_lon))

print("Done!")

# Get min value from timestamp time dummies
MIN_TIME_DUMMY = dataset["timestamp"].min()

# Update time dummies to go from 0 to max + min instead of from min to max
dataset["timestamp"] -= MIN_TIME_DUMMY

# Sort by timestamp and by phone ID
print("Sorting dataset...")

dataset.sort_values(
    by=["PHONE_ID", "timestamp"],
    inplace=True,
    ascending=True
)

print("Done!")


# Store updated dataset
print("Saving updated dataset...")

dataset.to_csv(
    path_or_buf=DATA_DIR / "updated_data.csv",
    index=False
)

print("Done!")