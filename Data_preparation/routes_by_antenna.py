import json
import pandas as pd
import numpy as np
import multiprocessing as mp

from pathlib import Path
from collections import defaultdict

from latlon_tools import distance_km
from utils.constants import DATA_DIR, DECIMALS
from utils.storers import CSVStorer

# Specify types of columns
DTYPE = {
    "PHONE_ID": "string",
    "bts_id": "string",
    "antenna id": np.int64,
    "timestamp": np.int64,
    "lat": np.int64,
    "lon": np.int64
}

# Specify dataframe iterator chunk size
CHUNKSIZE = 1e5


def groupby_antenna_id(dataset_chunk):
    values = []
    columns = [
        "phone id", "antenna id",
        "start", "stop",
        "lat", "lon",
        "dwell time", "jump time",
        "jump distance", "jump velocity"
    ]

    # Setup left pointer
    l = dataset_chunk.first_valid_index()

    # Setup initial jump values
    jump_time = np.nan
    jump_distance = np.nan
    jump_velocity = np.nan

    MAX_IDX = l + len(dataset_chunk)

    for r in range(l, MAX_IDX):
        i = min(r+1, MAX_IDX-1)

        # Get phone ID values
        phone_id_nxt = dataset_chunk["PHONE_ID"][i]
        phone_id_r = dataset_chunk["PHONE_ID"][r]

        # Get antenna ID values
        antenna_id_nxt = dataset_chunk["antenna id"][i]
        antenna_id_r = dataset_chunk["antenna id"][r]

        # Get timestamp values
        timestamp_l = dataset_chunk["timestamp"][l]
        timestamp_r = dataset_chunk["timestamp"][r]
        timestamp_nxt = dataset_chunk["timestamp"][i]

        # Get lat and lon values
        lat_r = dataset_chunk["lat"][r] / 10 ** DECIMALS
        lat_nxt = dataset_chunk["lat"][i] / 10 ** DECIMALS

        lon_r = dataset_chunk["lon"][r] / 10 ** DECIMALS
        lon_nxt = dataset_chunk["lon"][i] / 10 ** DECIMALS

        # Determine if a next antenna ID is different from current
        jumped = antenna_id_nxt != antenna_id_r

        # Flag for change of phone ID
        phone_id_switch = phone_id_nxt != phone_id_r

        # Determine if the end of the array's been reached
        is_end = r == i or phone_id_switch

        if jumped or is_end:
            dwell_time = (timestamp_r - timestamp_l) / 60  # Get dwell time in minutes

             # Normal update if phone is the same
            if not phone_id_switch:
                # Update jump time
                jump_time = (timestamp_nxt - timestamp_r) / 60  # Get jump time in minutes

                # Update jump distance
                jump_distance = distance_km(
                    (np.radians(lat_r), np.radians(lon_r)),
                    (np.radians(lat_nxt), np.radians(lon_nxt))
                )

                # Update jump velocity
                jump_velocity = np.nan if jump_time == 0 else jump_distance / jump_time * 60  # km/hr
            else:  # Reset values to NaN if phone ID changed
                jump_time = np.nan
                jump_distance = np.nan
                jump_velocity = np.nan

            values.append([
                phone_id_r,
                antenna_id_r,
                timestamp_l,
                timestamp_r,
                lat_r,
                lon_r,
                dwell_time,                
                jump_time,
                jump_distance,
                jump_velocity
            ])

            # Update left pointer
            l = i

    return pd.DataFrame(values, columns=columns)


if __name__ == "__main__":
    # Load updated data
    print("Loading updated dataset...")

    dataset_it = pd.read_csv(
        DATA_DIR / "updated_data.csv",
        dtype=DTYPE,
        chunksize=CHUNKSIZE,
        # nrows=1e6
    )

    print("Done!")

    # Perform multiprocessing
    print("Performing multiprocessing...")

    results = []

    with mp.Pool(processes=int(mp.cpu_count() * 3 / 4)) as pool:
        results = pool.map(groupby_antenna_id, dataset_it)

    print("Done!")

    print("Checking grouping...")

    # Check if grouping needs updates at the end and start of each result
    result_l = results[0]
    l = result_l.iloc[result_l.index[-1]]

    for result in results:
        drop_first = False

        r = result.iloc[result.index[0]]

        phone_id_l = l["phone id"]
        phone_id_r = r["phone id"]

        antenna_l = l["antenna id"]
        antenna_r = r["antenna id"]
        
        if phone_id_l == phone_id_r and antenna_l == antenna_r:
            start = l["start"]
            stop = r["stop"]

            dwell_time = (stop - start) / 60  # Convert to minutes

            jump_time = r["jump time"]
            jump_distance = r["jump distance"]
            jump_velocity = r["jump velocity"]

            if jump_time == np.nan and jump_distance == np.nan and jump_velocity == np.nan:
                i = result.iloc[result.index[1]]  # Get next row after right-pointer row

                lat_r = r["lat"]
                lon_r = r["lon"]

                lat_i = i["lat"]
                lon_i = i["lon"]

                if i["phone id"] == r["phone id"]:
                    jump_time = (i["start"] - r["stop"]) / 60  # Convert to minutes
                    jump_distance = distance_km(
                        (np.radians(lat_r), np.radians(lon_r)),
                        (np.radians(lat_i), np.radians(lon_i))
                    )
                    jump_velocity = np.nan if jump_time == 0 else jump_distance / jump_time * 60  # km/hr
                else:
                    jump_time = np.nan
                    jump_distance = np.nan
                    jump_velocity = np.nan

            # Update left-pointer row
            result_l.loc[
                result_l.index == result_l.index[-1],
                ["stop", "dwell time", "jump time", "jump distance", "jump velocity"]
            ] = [stop, dwell_time, jump_time, jump_distance, jump_velocity]

            # Drop first row (right pointer row)
            result.drop(result.index[0], inplace=True)
            result.reset_index(drop=True, inplace=True)

        l = result.iloc[result.index[-1]]
        result_l = result

    print("Done!")
    
    # Concat results from multiprocessing
    print("Concatenating multiprocessing results...")

    routes_ready = pd.concat(results)

    print("Done!")

    # Verify that phone IDs are indeed sorted
    print("Phone IDs are sorted?", "Yes" if routes_ready["phone id"].is_monotonic_increasing else "No")

    # Save dataframe to CSV
    print("Storing dataframe in CSV file...")    

    CSVStorer("routes_ready", routes_ready).store()
        
    print("Done!")
