import pandas as pd

from pathlib import Path

DTYPE = {
    "lat": "string",  # Handling lat as string avoids floating precision errors
    "lon": "string"  # Handling lon as string avoids floating precision errors
}

DATA_DIR = Path("data")  # Define directory for datasets

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

# Each phone id will have a route (a list), which is composed of mobile connections
phone_id_route = defaultdict(list)

# Map bts_ids to coordinates
bts_latlon = {}

# Retrieve info for each mobile connection associated with a phone id
print("Retrieving mobile connections...")

for i in dataset.index:
    # Get values by index
    phone_id = dataset["PHONE_ID"][i]
    timestamp = dataset["timestamp"][i]

    lat = dataset["lat"][i]
    lon = dataset["lon"][i]

    bts_id = dataset["bts_id"][i]

    # Only consider the lat and lon of the first bts_id instance
    if bts_id in bts_latlon:
        lat = bts_latlon[bts_id][0]
        lon = bts_latlon[bts_id][1]
    else:
        bts_latlon[bts_id] = (lat, lon)

    phone_id_route[phone_id].append((timestamp, lat, lon))

print("Done!")

# Specify time format by which timestamp strings will be parsed
TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"

# Sort mobile connections by timestamp
print("Sorting mobile connections by timestamp...")

for key in phone_id_route.keys():
    phone_id_route[key].sort(
        # Parse timestamp strings to datetime objects
        key=lambda mobile_connection: datetime.strptime(
            mobile_connection[0],
            TIME_FORMAT
        )
    )
    
print("Done!")

# Store dict in JSON file
import os

# Create directory to store JSON file
JSON_DIR = Path("json/routes")

try:
    os.mkdir(JSON_DIR)
except FileExistsError:
    print("Directory already exists")
except:
    # Abort program in case other exceptions occur
    raise Exception("Directory could not be created")

# Store routes JSON file
print("Storing JSON files...")

with open(JSON_DIR / "routes.json", "w") as f:
    json.dump(phone_id_route, f)

print("Done!")

# Print number of phone ids in dataset
print("# of phone IDs:", len(phone_id_route))