import pandas as pd
import geopandas as gpd
import os
import json

from shapely.geometry import Point, Polygon
from collections import defaultdict
from pathlib import Path


def get_comunas_bts_dict(antenna_df, comunas_geodata):
    # Create list of comunas to insert later as a column in antenna_df
    comunas = []

    for i in antenna_df.index:
        # Get lat and lon strings
        lat = antenna_df["lat"][i]
        lon = antenna_df["lon"][i]

        # Get bts_id by index
        bts_id = antenna_df["bts_id"][i]

        # Convert lat and lon to string
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

    # Sort by bts_id in descending order
    antenna_df.sort_values(by=["comuna", "bts_id"], inplace=True, ascending=True)

    # Store antenna geolocation dataframe
    DATA_DIR = Path("data")

    # Check if directory exists
    try:
        os.mkdir(DATA_DIR)
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
        "bts_id": "string",
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
    dataset.drop_duplicates(subset=["bts_id"], inplace=True, keep="first")
    
    # Drop phone and timestamp data to work only with antenna data
    dataset.drop(["PHONE_ID", "timestamp"], axis=1, inplace=True)

    #load map data
    MAP_LOC = DATA_DIR / Path("santiago-chile-shape-files")
    
    print("Loading shapefile")

    comunas_geodata = gpd.read_file(MAP_LOC / "COMUNA_C17.shp")
    
    print('Done!')

    #generate comunas and bts dict
    get_comunas_bts_dict(dataset, comunas_geodata)
