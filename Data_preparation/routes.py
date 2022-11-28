import os
import pandas as pd
import numpy as np

from pathlib import Path

from utils.constants import DECIMALS, JSON_DIR, DATA_DIR, KM_TO_M

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
dataset["timestamp"] = dataset["timestamp"].dt.total_seconds().astype(np.int64)

# Get min value from timestamp time dummies
MIN_TIME_DUMMY = dataset["timestamp"].min()

# Update time dummies to go from 0 to max + min instead of from min to max
dataset["timestamp"] -= MIN_TIME_DUMMY

print("Done!")

# Add ID per antena based on distance between lat and lon random pair
print("Computing ID for every antena...")

dataset["antenna id"] = dataset["lat"] - dataset["lon"]
dataset["antenna id"] *= 10 ** DECIMALS
dataset["antenna id"] = dataset["antenna id"].astype(np.int64)
dataset["antenna id"] -= dataset["antenna id"].min()

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