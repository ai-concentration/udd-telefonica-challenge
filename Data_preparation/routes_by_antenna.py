import json
import pandas as pd
import numpy as np

from pathlib import Path
from latlon_tools import distance_km

from utils.constants import DATA_DIR

# Specify types of columns
DTYPE = {
    "PHONE_ID": "string",
    "bts_id": "string",
    "antenna id": np.int64,
    "timestamp": np.int64,
    "lat": np.int64,
    "lon": np.int64
}

# Load updated data
print("Loading updated dataset...")

updated_dataset = pd.read_csv(
    DATA_DIR / "updated_data.csv",
    dtype=DTYPE
)

print("Done!")

from collections import defaultdict

# Define dictionary to store routes grouped by antennas
routes_ready = defaultdict(list)

# Keep track of current index
idx = 0

# Setup two pointers
l = 0
r = 0

# Setup jump values to NaN
jump_time = np.nan
jump_distance = np.nan
jump_velocity = np.nan

# Get dataset entries
ENTRIES = len(updated_dataset.index)

# Keep track of phone ID changes with flag
phone_id_tail = False

# Group routes by antenna
print("Grouping antennas in routes...")

for i in updated_dataset.index:
    # Update pointer and jump values when phone ID changes
    if phone_id_tail:
        # Update pointers
        l = i
        r = i

        # Update jump values
        jump_time = np.nan
        jump_distance = np.nan
        jump_velocity = np.nan

    # Get current phone ID
    phone_id = updated_dataset["PHONE_ID"][i]    

    # Get next index
    j = min(i+1, ENTRIES-1)

    # Get next phone ID
    phone_id_nxt = updated_dataset["PHONE_ID"][j]

    # Get current timestamp and lat/lon values
    timestamp_now = updated_dataset["timestamp"][i]

    lat_now = updated_dataset["lat"][i]
    lon_now = updated_dataset["lon"][i]

    # Get left and right pointer timestamps and lat/lon values
    timestamp_l = updated_dataset["timestamp"][l]
    timestamp_r = updated_dataset["timestamp"][r]

    lat_l = updated_dataset["lat"][l]
    lat_r = updated_dataset["lat"][r]

    lon_l = updated_dataset["lon"][l]
    lon_r = updated_dataset["lon"][r]

    # Determine if antennas from left pointer to right pointer should be grouped
    jumped = lat_now != lat_r and lon_now != lon_r
    phone_id_tail = phone_id != phone_id_nxt or j == ENTRIES - 1

    # Group entires with same antena
    if jumped or phone_id_tail:
        dwell_time = (timestamp_r - timestamp_l) / 60  # Get dwell time in minutes

        # Append values to dictionary
        routes_ready["phone id"].append(phone_id)

        routes_ready["start"].append(timestamp_l)
        routes_ready["stop"].append(timestamp_r)

        routes_ready["lat"].append(lat_r)
        routes_ready["lon"].append(lon_r)

        routes_ready["dwell time"].append(dwell_time)

        routes_ready["jump time"].append(jump_time)
        routes_ready["jump distance"].append(jump_distance)
        routes_ready["jump velocity"].append(jump_velocity)

        # Update jump time
        jump_time = (timestamp_now - timestamp_r) / 60  # Get jump time in minutes

        # Update jump distance
        jump_distance = distance_km(
            # Lat and lon values pass form strings to float
            (np.radians(float(lat_r)), np.radians(float(lon_r))),  # Convert to radians
            (np.radians(float(lat_now)), np.radians(float(lon_now)))  # Convert to radians
        )

        # Update jump velocity
        jump_velocity = np.nan if jump_time == 0 else jump_distance / jump_time * 60  # To km/hr

        # Update left pointer
        l = i

    idx += 1

    r = i  # Update right pointer
            
print("Done!")

# Convert dict to dataframe
routes_ready = pd.DataFrame(data=routes_ready)

# Save dataframe to CSV
print("Storing dataframe in CSV file...")

from utils.storers import CSVStorer

CSVStorer("routes_ready", routes_ready).store()
    
print("Done!")