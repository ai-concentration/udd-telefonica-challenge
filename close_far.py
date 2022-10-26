import numpy as np
import pandas as pd
import json
import os

from pathlib import Path

from latlon_tools import distance_km

DTYPE = {
    "lat": "string",  # Handling lat as string avoids floating precision errors
    "lon": "string"  # Handling lon as string avoids floating precision errors
}

DATA_DIR = Path("data")

# Load antenna geolocation dataset due to smaller size
print("Loading dataset...")

# Load dataset
dataset = pd.read_csv(DATA_DIR / 'antenna_geolocation.csv', dtype=DTYPE)

print("Done!")

max_distance = 0
min_distance = 10000
key = ""
closest = ["",""]
far = ["",""]
dic = {}

print("Getting closest and farthest from each antenna...")

for i in dataset.index:
    distances = []
    for j in dataset.index:
        if i == j:  # Continue if same index, otherwise distance and min will be 0!
            continue

        distance = distance_km(
            (np.radians(float(dataset['lat'][i])), np.radians(float(dataset['lon'][i]))),
            (np.radians(float(dataset['lat'][j])), np.radians(float(dataset['lon'][j])))
        )
        #distances.append(distance)
        if distance > max_distance:
            far = [dataset['lat'][j],dataset['lon'][j]]
            max_distance = distance
        if distance < min_distance:
            closest = [dataset['lat'][j],dataset['lon'][j]]
            min_distance = distance
  
    #dic = {str((dataset['lat'][i], dataset['lon'][i])): far, closest}
    key = f"{dataset['lat'][i]},{dataset['lon'][i]}"
    dic[key] = far, closest

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
print("Making JSON file...")

with open(JSON_DIR / "closest_farthest.json", "w") as f:
    json.dump(dic, f)
    
print("Done!")