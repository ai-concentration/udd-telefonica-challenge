import json

from pathlib import Path
from latlon_tools import distance_km

# JSON files are stored in json dir
JSON_DIR = Path("json/routes")

# Load JSON file
routes = None

print("Loading JSON file...")

with open(JSON_DIR / "routes.json", "r") as f:
    routes = json.load(f)

print("Done!")

from collections import defaultdict
from datetime import datetime  # To parse timestamp strings

# Specify time format by which timestamp strings will be parsed
TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"

# Define dictionary to store routes grouped by antennas
import pandas as pd

routes_ready = defaultdict(list)
# routes_ready = pd.DataFrame(
#     columns=[
#         "phone id",
#         "start",
#         "end",
#         "lat",
#         "lon",        
#         "dwell time",
#         "jump time",
#         "jump distance",
#         "jump velocity"
#     ]
# )

# Epsilon value to compare floats
EPSILON = 1e-5

import numpy as np

# Group routes by antenna
print("Grouping antennas in routes...")

for phone_id, route in routes.items():
    route_size = len(route)

    l = 0  # Left pointer
    r = 0  # Right pointer

    # Set jump values to NaN
    jump_time = np.nan
    jump_distance = np.nan
    jump_velocity = np.nan
    
    for i in range(0, route_size):
        timestamp_lo, lat_lo, lon_lo = route[l]
        timestamp_hi, lat_hi, lon_hi = route[r]

        timestamp_nxt, lat_nxt, lon_nxt = route[i]

        jumped = abs(lat_nxt - lat_hi) > EPSILON and abs(lon_nxt - lon_hi) > EPSILON
        is_tail = i == route_size - 1

        # Make float comparison: If different, then antenna has changed
        if jumped or is_tail:
            timestamp_lo = datetime.strptime(timestamp_lo, TIME_FORMAT)
            timestamp_hi = datetime.strptime(timestamp_hi, TIME_FORMAT)

            timestamp_nxt = datetime.strptime(timestamp_nxt, TIME_FORMAT)

            dwell_time = timestamp_hi - timestamp_lo
            dwell_time = dwell_time.total_seconds() / 60  # Convert to minutes

            # Append values to dictionary
            routes_ready["phone id"].append(phone_id)
            
            routes_ready["start"].append(datetime.strftime(timestamp_lo, TIME_FORMAT))  # start
            routes_ready["end"].append(datetime.strftime(timestamp_hi, TIME_FORMAT))  # end
            
            routes_ready["lat"].append(lat_hi)
            routes_ready["lon"].append(lon_hi)
            
            routes_ready["dwell time"].append(dwell_time)

            routes_ready["jump time"].append(jump_time)
            routes_ready["jump distance"].append(jump_distance)
            routes_ready["jump velocity"].append(jump_velocity)
            
            # Update jump values
            jump_time = timestamp_nxt - timestamp_hi
            jump_time = jump_time.total_seconds() / 60  # Convert to minutes

            jump_distance = distance_km(
                (np.radians(lat_hi), np.radians(lon_hi)),  # Convert to radians
                (np.radians(lat_nxt), np.radians(lon_nxt)),  # Convert to radians
            )
            # Over 60 to get km/hr instead of km/min
            jump_velocity = np.nan if jump_time == 0 else jump_distance / jump_time / 60

            # Update left pointer
            l = i

        # Update right pointer
        r = i
            
print("Done!")

# Convert dict to dataframe
routes_ready = pd.DataFrame(data=routes_ready)

# Create dir to store dataframe's CSV
import os

DATA_DIR = Path("data")

try:
    os.mkdir(DATA_DIR)
except FileExistsError:
    print("Directory already exists")
except:
    # Abort program in case other exceptions occur
    raise Exception("Directory could not be created")

# Save dataframe to CSV
print("Storing dataframe in CSV file...")

routes_ready.to_csv(path_or_buf=DATA_DIR / "routes_ready.csv", index=False)
    
print("Done!")