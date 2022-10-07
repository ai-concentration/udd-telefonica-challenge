import pandas as pd

from pathlib import Path

DATA_DIR = Path("data")  # Define directory for datasets

# Loading the dataset
print("Loading dataset...")

dataset = pd.read_csv(DATA_DIR / "data.csv")

print("Done!")

import json

from collections import defaultdict
from datetime import datetime  # So we can deal with timestamps strings

# Each phone id will have a route (a list), which is composed of mobile connections
phone_id_route = defaultdict(list)

# Retrieve info for each mobile connection associated with a phone id
print("Retrieving mobile connections...")

for i in dataset.index:
    # Get values by index
    phone_id = dataset["PHONE_ID"][i]
    timestamp = dataset["timestamp"][i]
    antenna_id = dataset["bts_id"][i]

    phone_id_route[phone_id].append((timestamp, antenna_id))

print("Done!")

# Specify time format by which timestamp strings will be parsed
TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"

# Sort mobile connections by timestamp
print("Sorting mobile connections...")

for key in phone_id_route.keys():
    phone_id_route[key].sort(
        # Parse timestamp strings to datetime objects
        key=lambda mobile_connection: datetime.strptime(
            mobile_connection[0],
            TIME_FORMAT
        )
    )
    
print("Done!")

# Create directory to store JSON files
JSON_DIR = Path("json")

try:
    os.mkdir(JSON_DIR)
except FileExistsError:
    print("Directory already exists")
except:
    # Abort program in case other exceptions occur
    raise Exception("Directory could not be created")

# Store defaultdict in JSON file
print("Storing routes in JSON file...")

with open(JSON_DIR / "routes.json", "w") as f:
    json.dump(phone_id_route, f)
    
print("Done!")

# Print number of phone ids in dataset
print(len(phone_id_route))