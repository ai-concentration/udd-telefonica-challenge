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


def groupby_antenna_id(phone_id_group):
    updated_dataset, phone_id, idx_range = phone_id_group

    values = []
    columns = [
        "phone id", "antenna id",
        "start", "stop",
        "lat", "lon",
        "dweel time", "jump time",
        "jump distance", "jump velocity"
    ]

    # Setup left pointer
    l = idx_range[0]

    # Setup initial jump values
    jump_time = np.nan
    jump_distance = np.nan
    jump_velocity = np.nan

    # Get max index
    MAX_IDX = idx_range[-1]

    for r in idx_range:
        i = min(r+1, MAX_IDX)

        # Get antenna ID values
        antenna_id_nxt = updated_dataset["antenna id"][i]
        antenna_id_r = updated_dataset["antenna id"][r]

        # Get timestamp values
        timestamp_l = updated_dataset["timestamp"][l]
        timestamp_r = updated_dataset["timestamp"][r]
        timestamp_nxt = updated_dataset["timestamp"][i]

        # Get lat and lon values
        lat_r = updated_dataset["lat"][r] / 10 ** DECIMALS
        lat_nxt = updated_dataset["lat"][i] / 10 ** DECIMALS

        lon_r = updated_dataset["lon"][r] / 10 ** DECIMALS
        lon_nxt = updated_dataset["lon"][i] / 10 ** DECIMALS

        # Determine if a next antenna ID is different from current
        jumped = antenna_id_nxt != antenna_id_r

        # Determine if the end of the array's been reached
        is_end = r == i

        if jumped or is_end:
            dwell_time = (timestamp_r - timestamp_l) / 60  # Get dwell time in minutes

            values.append([
                phone_id,
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

            # Update jump time
            jump_time = (timestamp_nxt - timestamp_r) / 60  # Get jump time in minutes

            # Update jump distance
            jump_distance = distance_km(
                (np.radians(lat_r), np.radians(lon_r)),
                (np.radians(lat_nxt), np.radians(lon_nxt))
            )

            # Update jump velocity
            jump_velocity = np.nan if jump_time == 0 else jump_distance / jump_time * 60  # km/hr

            # Update left pointer
            l = i

    return pd.DataFrame(values, columns=columns)


if __name__ == "__main__":
    # Load updated data
    print("Loading updated dataset...")

    updated_dataset = pd.read_csv(
        DATA_DIR / "updated_data.csv",
        dtype=DTYPE
    )

    print("Done!")

    # Retrieving phone ID groups
    print("Retrieving phone ID groups...")

    phone_id_groups = [
        (updated_dataset, phone_id, idx_range)
        for phone_id, idx_range in updated_dataset.groupby(
            ["PHONE_ID"], sort=False
        ).groups.items()
    ]

    print("Done!")

    # Perform multiprocessing
    print("Performing multiprocessing...")

    results = []

    with mp.Pool(processes=int(mp.cpu_count() * 3 / 4)) as pool:
        results = pool.map(groupby_antenna_id, phone_id_groups)

    print("Done!")

    # Concat results from multiprocessing
    print("Concatenating multiprocessing results...")

    routes_ready = pd.concat(results)

    print("Done!")

    # Save dataframe to CSV
    print("Storing dataframe in CSV file...")    

    CSVStorer("routes_ready", routes_ready).store()
        
    print("Done!")