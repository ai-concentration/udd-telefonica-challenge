import numpy as np
import pandas as pd
import json
import os

from pathlib import Path

from latlon_tools import distance_km

DATA_DIR = Path("data")

dtype = {
    'lat': 'string',  # Handle as string to avoid floating precision errors
    'lon': 'string',  # Handle as string to avoid floating precision errors
}

dataset = pd.read_csv(DATA_DIR / 'data.csv', dtype=dtype)

max_distance = 0
min_distance = 10000
key = ""
closest = ["",""]
far = ["",""]
dic = {}
for i in range(len(dataset['bts_id'])):
    distances = []
    for j in range(len(dataset['bts_id'])):
        distance = DistanceKm(dataset['lat'][i],dataset['lon'][i],dataset['lat'][j],dataset['lon'][j])
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
    json.dump(dic, f,skipkeys=True)
    
print("Done!")