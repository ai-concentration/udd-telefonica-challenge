import pandas as pd
import geopandas as gpd
import os
import json

from shapely.geometry import Point, Polygon
from collections import defaultdict
from pathlib import Path


def get_comunas_bts_dict(antenna_df, comunas_geodata):
    # Define dictionary to store all bts related to an antenna
    antenna_bts = defaultdict(list)
    
    # Create list of comunas to insert later as a column in antenna_df
    comunas = []

    for i in antenna_df.index:
        # Get lat and lon strings
        lat = antenna_df["lat"][i]
        lon = antenna_df["lon"][i]

        # Get bts_id by index
        bts_id = antenna_df["bts_id"][i]

        # Get antenna id
        antenna_id = f"{lat},{lon}"

        # Add bts_id to antenna
        antenna_bts[antenna_id].append(bts_id)

        # Convert lat and lon from strings to floats
        lat = float(lat)
        lon = float(lon)

        # Create geopandas Point to determine comuna
        antenna_loc = Point(lon, lat)

        # Get comuna that contains the antenna
        for comuna, geometry in zip(
            comunas_geodata["NOM_COMUNA"], comunas_geodata["geometry"]
        ):
            # It is guaranteed at least one comuna will match
            if geometry.contains(antenna_loc):
                comunas.append(comuna)
                break

    antenna_df["comuna"] = comunas

    # Create directory to store JSON file
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

    with open(JSON_DIR / "antenna_bts.json", "w") as f:
        json.dump(antenna_bts, f)
        
    print("Done!")

    # Store antenna geolocation dataframe
    DATA_DIR = Path("data")

    # Check if directory exists
    try:
        os.mkdir(JSON_DIR)
    except FileExistsError:
        print("Directory already exists")
    except:
        # Abort program in case other exceptions occur
        raise Exception("Directory could not be created")

    antenna_df.to_csv(path_or_buf=DATA_DIR / "antenna_geolocation.csv", index=False)

if __name__ == '__main__':
    # Define dataset column dtypes
    DATA_DTYPE = {
        "PHONE_ID": "string",
        "timestamp": "string",
        "bts_id": "category",
        "lat": "string",  # Handling lat as string avoids floating precision errors
        "lon": "string"  # Handling lon as string avoids floating precision errors
    }
    
    #load dataset
    DATA_DIR = Path("data")
    
    print("Loading dataset..")

    dataset = pd.read_csv(
        DATA_DIR / 'data.csv',
        dtype=DATA_DTYPE
    )  
    
    print('Done!')

    # Drop duplicate bts_ids
    dataset.drop_duplicates(subset=["bts_id"], inplace=True)
    
    # Drop phone and timestamp data to work only with antenna data
    dataset.drop(["PHONE_ID", "timestamp"], axis=1, inplace=True)

    #load map data
    MAP_LOC = DATA_DIR / Path("santiago-chile-shape-files")
    
    print("Loading shapefile")

    comunas_geodata = gpd.read_file(MAP_LOC / "COMUNA_C17.shp")
    
    print('Done!')

    #generate comunas and bts dict
    get_comunas_bts_dict(dataset, comunas_geodata)
