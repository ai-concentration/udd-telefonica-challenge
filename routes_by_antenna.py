import json

from pathlib import Path

# JSON files are stored in json dir
JSON_DIR = Path("json")

# Load JSON file
routes = None

with open(JSON_DIR / "phone_id_route.json", "r") as f:
    routes = json.load(f)

from collections import defaultdict
from datetime import datetime  # To parse timestamp strings

# Specify time format by which timestamp strings will be parsed
TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"

# Define dictionary to store routes grouped by antennas
routes_by_antenna = defaultdict(list)

# Group routes by antenna
print("Grouping antennas in routes...")

for phone_id, route in data.items():
    timestamp_lo, antenna_now = route[0]
    
    len_route = len(route)
    
    for i in range(1, len_route):
        timestamp_hi, antenna = route[i]
        
        # If the antenna is different, then get connection times from previous antenna
        if antenna != antenna_now or i == len_route - 1:
            delta_seconds = (
                datetime.strptime(
                    timestamp_hi,
                    TIME_FORMAT
                )
                - datetime.strptime(
                    timestamp_lo,
                    TIME_FORMAT
                )
            ).total_seconds() / 60  # From microseconds to seconds
            
            routes_by_antenna[phone_id].append((timestamp_lo, timestamp_hi, delta_seconds, antenna_now))
            
            # Update start timestamp and antenna
            timestamp_lo = timestamp_hi
            antenna_now = antenna
            
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

# Store routes by antenna in JSON file
print("Storing routes by antenna in JSON file...")

with open(JSON_DIR / "phone_id_routes_clean.json", "w") as f:
    json.dump(data_clean, f)
    
print("Done!")