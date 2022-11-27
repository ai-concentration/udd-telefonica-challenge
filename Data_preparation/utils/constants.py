import pandas as pd
import numpy as np

from pathlib import Path

# Path related constants
DATA_DIR = Path("data")
JSON_DIR = Path("json")

# Dataframe related constants for data.csv
DTYPE_DATA_DF = {
    "PHONE_ID": "string",
    "timestamp": "datetime64[ns, UTC]",
    "bts_id": "string",
    "lat": np.float64,
    "lon": np.float64
}

# Specify types of columns for updated_data.csv
DTYPE_UPDATED_DF = {
    "PHONE_ID": "string",
    "bts_id": "string",
    "antenna id": np.int64,
    "timestamp": np.int64,
    "lat": np.float64,
    "lon": np.float64
}

# Specify types of columns for routes_ready.csv
DTYPE_READY_DF = {
    "phone id": "string",
    "antenna id": np.int64,
    "start": np.int64,
    "stop": np.int64,
    "lat": np.float64,
    "lon": np.float64,
    "dwell time": np.float64,
    "jump time": np.float64,
    "jump distance": np.float64,
    "jump velocity": np.float64
}

# bts_id,lat,lon,antenna id,comuna
# Specify types of columns for routes_ready.csv
DTYPE_ANTENNA_DF = {
    "bts_id": "string",
    "lat": np.float64,
    "lon": np.float64,
    "antenna id": np.int64,
    "comuna": "string"
}

# Constant to specify chunk size when reading dataframes by chunk
CHUNKSIZE = 1e5  # For datasets over a 1M entries

# Data transformation related
DECIMALS = 4

# Unit conversion
KM_TO_M = 1e3

if __name__ == "__main__":
    pass