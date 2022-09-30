import os
import requests

from dotenv import load_dotenv
from pathlib import Path

# Load environmental vairables (Google Maps API key is treated as environmental variable)
DOTENV_PATH = Path(".keys")

load_dotenv(dotenv_path=DOTENV_PATH)

# Load API key from environmental variable
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# Load dataset provided by UDD and Telefonica
import pandas as pd

DATA_DIR = Path("data")

print("Loading dataset...")

dataset = pd.read_csv(
    DATA_DIR / "data.csv",
    # parse_dates=["timestamp"]  # Parsing dates is expensive!
)

print("Done!")

# Geocode latitude and longitude from first row
frow = dataset.iloc[0]

lat, lon = frow.lat, frow.lon

# Request reverse geocoding
ENDPOINT = "https://maps.googleapis.com/maps/api/geocode/json?"  # Retrieve as JSON

params = {
    "latlng": f"{lat},{lon}",
    "location_type": "ROOFTOP",  # Get only location information accurate down to street address precission
    "key": GOOGLE_MAPS_API_KEY
}

response = requests.get(
    ENDPOINT,
    params=params
)


def reverse_geocoding(lat, lon):
    # Request reverse geocoding
    ENDPOINT = "https://maps.googleapis.com/maps/api/geocode/json?"  # Retrieve as JSON

    params = {
        "latlng": f"{lat},{lon}",
        "location_type": "ROOFTOP",  # Get only location information accurate down to street address precission
        "key": GOOGLE_MAPS_API_KEY
    }

    return requests.get(
        ENDPOINT,
        params=params
    )


from collections import defaultdict, Counter


def get_comuna(json_response):
    results = json_response["results"]  # Get reverse geocoding results from response
    
    COMUNA_KEYWORDS = ["locality", "administrative_area_level_3"]  # Google Maps API identifies comunas by these keywords
    
    comunas = defaultdict(int)  # Define comuna counter
    
    for result in results:
        for address_component in result["address_components"]:
            # Ignore address components that are not comuna keywords
            for keyword in COMUNA_KEYWORDS:
                if keyword in address_component["types"]:
                    # Retrieve comunas always by long name
                    comunas[address_component["long_name"]] += 1
                
    # Return most common comuna in case of multiple comunas
    return Counter(comunas).most_common(1)


import json

# Create directory to store JSON files from responses
JSON_DIR = Path("reverse-geocoding-responses")

try:
    os.mkdir(JSON_DIR)
except FileExistsError:
    print("Directory already exists")
except:
    # Abort program if nothing in case other exceptions occur
    raise Exception("Directory could not be created")

# Define dataframe to store antennas geolocation
antennas_geolocation = pd.DataFrame(columns=["bts_id", "lat", "lon", "comuna"])

# Get antenna data from dataset
antennas = (
    dataset.drop_duplicates(subset=["bts_id"])  # Remove any duplicate antennas
    .drop(["PHONE_ID", "timestamp"], axis=1)  # Remove phone and timestamp columns
)

# # Check if antennas are assigned more than one latitude-longitude coordinate
# assert len(antennas) == len(dataset.drop_duplicates(subset=["bts_id", "lat", "lon"])), "There is more than one latitude-longitude coordinate assigned to each antenna"

print(antennas.columns)  # Get column names
print(dataset.columns)  # Get column names

import numpy as np


def responses_google_maps(antennas):
    # Retrieve Google Maps API responses
    print("Retrieving responses...")

    for i, row in antennas.iterrows():
        rlat, rlon = row.lat, row.lon
        antenna_id = row.bts_id
        
        # Get reverse geocoding response
        response = reverse_geocoding(rlat, rlon)
        
        # Verify response is successful (status code between 200 and 400)
        while not response:
            response = reverse_geocoding(rlat, rlon)
        
        # Get comuna from response's JSON
        comuna = get_comuna(response.json())
        
        # Check if location could be retrieved and process it accordingly
        if comuna:
            comuna = comuna[0][0]  # Get tuple from 1-value list and value from value-count tuple
        else:
            comuna = np.nan
        
        # Add geolocation info to geolocation dataframe
        antennas_geolocation.loc[len(antennas_geolocation)] = [antenna_id, rlat, rlon, comuna]
        
        # Set path to store JSON
        json_path = JSON_DIR / f"{antenna_id}.json"
        
        # Store JSON from response
        with open(json_path, "w") as f:
            json.dump(response.json(), f)
            
    print("Done!")


def responses_local(antennas):
    # Read Google Maps API responses from local dir
    print("Retrieving responses...")

    for i, row in antennas.iterrows():
        rlat, rlon = row.lat, row.lon
        antenna_id = row.bts_id
        
        # Load JSON data from Google Maps API response
        json_file = None
        
        with open(JSON_DIR / f"{antenna_id}.json", "r") as f:
            json_file = json.load(f)
        
        # Get comuna from response's JSON
        comuna = get_comuna(json_file)
        
        # Check if location could be retrieved and process it accordingly
        if comuna:
            comuna = comuna[0][0]  # Get tuple from 1-value list and value from value-count tuple
        else:
            comuna = np.nan
        
        # Add geolocation info to geolocation dataframe
        antennas_geolocation.loc[len(antennas_geolocation)] = [antenna_id, rlat, rlon, comuna]
            
    print("Done!")


# Create dataframe from local responses; if you prefer to use Google Maps API, use responses_google_maps
responses_local(antennas)

# Get antennas geolocation info
print(antennas_geolocation.info())

# Verify that all antennas have been reverse-geocoded
assert len(antennas_geolocation) == len(antennas), "Not every antenna was reverse-geocoded"

# Save dataframe to csv
antennas_geolocation.to_csv(path_or_buf=DATA_DIR / "antennas_geolocation.csv", index=False)

# Print NAN values (specially for comunas)
print(antennas_geolocation.isna().sum())