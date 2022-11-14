import os
import pandas as pd
import numpy as np

from pathlib import Path

from utils.constants import DECIMALS, DATA_DTYPE, JSON_DIR, DATA_DIR, KM_TO_M

# Loading the dataset
print("Loading dataset...")

dataset = pd.read_csv(DATA_DIR / "data.csv")

print("Done!")

import json

from collections import defaultdict  # apply method performs in parallel

# Convert timestamp datetimes total seconds
print("Updating timestamp column...")

dataset["timestamp"] = pd.to_datetime(
    dataset["timestamp"],
    utc=True,
    infer_datetime_format=True
)

dataset["timestamp"] = dataset["timestamp"] - dataset["timestamp"][0]
dataset["timestamp"] = dataset["timestamp"].dt.total_seconds().astype(int)

# Get min value from timestamp time dummies
MIN_TIME_DUMMY = dataset["timestamp"].min()

# Update time dummies to go from 0 to max + min instead of from min to max
dataset["timestamp"] -= MIN_TIME_DUMMY

print("Done!")

# Add ID per antena based on distance between lat and lon random pair
print("Computing ID for every antena...")

LAT_LON_ORIGIN = (dataset["lat"][0], dataset["lon"][0])
EARTH_RADIUS = 6371  # In kilometers

lat_rad = np.radians(dataset["lat"])
lon_rad = np.radians(dataset["lon"])

lat_delta = lat_rad - LAT_LON_ORIGIN[0]
lon_delta = lon_rad - LAT_LON_ORIGIN[1]

arc = np.sin(lat_delta / 2) ** 2 + np.cos(LAT_LON_ORIGIN[0]) \
    * np.sin(lon_delta / 2) ** 2 * np.cos(lat_rad)

dataset["antenna id"] = 2 * EARTH_RADIUS * np.arctan2(np.sqrt(arc), np.sqrt(1 - arc))
dataset["antenna id"] *= KM_TO_M
dataset["antenna id"] = dataset["antenna id"].astype(np.int64)

MIN_ANTENNA_ID = dataset["antenna id"].min()

dataset["antenna id"] -= MIN_ANTENNA_ID

print("Done!")

# Update lat and lon columns to be integers
print("Converting float columns to integer columns...")

dataset["lat"] *= 10 ** DECIMALS
dataset["lon"] *= 10 ** DECIMALS

dataset["lat"] = dataset["lat"].astype(np.int64)
dataset["lon"] = dataset["lon"].astype(np.int64)

print("Done!")

# Sort by timestamp and by phone ID
print("Sorting dataset...")

dataset.sort_values( 
    by=["PHONE_ID", "timestamp"],
    inplace=True,
    ascending=True
)

print("Done!")

from utils.storers import CSVStorer

# Store updated dataset
print("Saving updated dataset...")

CSVStorer("updated_data", dataset).store()

print("Done!")