import pandas as pd
import numpy as np

from pathlib import Path

# Path related constants
DATA_DIR = Path("data")
JSON_DIR = Path("json")

# Dataframe related constants
DATA_DTYPE = {
    "PHONE_ID": "string",
    "timestamp": "datetime64[ns, UTC]",
    "bts_id": "string",
    "lat": np.float64,
    "lon": np.float64
}

# Data transformation related
DECIMALS = 4

# Unit conversion
KM_TO_M = 1e3

if __name__ == "__main__":
    pass