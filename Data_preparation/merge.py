import pandas as pd

from utils.constants import DATA_DIR, DTYPE_READY_DF, CHUNKSIZE, DTYPE_ANTENNA_DF


if __name__ == "__main__":
    ready_df = pd.read_csv(
        DATA_DIR / "routes_ready.csv",
        dtype=DTYPE_READY_DF,
        chunksize=CHUNKSIZE,
        # nrows=1e6  # Work only with a small set for testing
    )

    antenna_df = pd.read_csv(
        DATA_DIR / "antenna_geolocation.csv",
        dtype=DTYPE_ANTENNA_DF
    )
    population_df = pd.read_csv(DATA_DIR / "population_by_comuna.csv")

    population_df.drop("Variable", axis=1, inplace=True)
    population_df["Unidad territorial"] = population_df["Unidad territorial"].str.lower()  # Lower case for easier processing    

    for i, chunk in enumerate(ready_df):
        # Get population by comuna
        chunk["population"] = chunk["antenna id"].apply(
            lambda x: population_df.loc[
                population_df["Unidad territorial"] == antenna_df.loc[
                    antenna_df["antenna id"] == x
                ]["comuna"].values[0]
            ]["2017"].values[0]  # Values is guaranteed to be a 1-element array
        )
        # Get comuna
        chunk["comuna"] = chunk["antenna id"].apply(
            lambda x: antenna_df.loc[
                antenna_df["antenna id"] == x
            ]["comuna"].values[0]
        )

        if i == 0:  # Store with header
            chunk.to_csv(
                DATA_DIR / "model_dataset.csv",
                index=False,
                mode="a"  # Append to existing CSV file
            )
        else:  # Ignore header
            chunk.to_csv(
                DATA_DIR / "model_dataset.csv",
                header=None,
                index=False,
                mode="a"  # Append to existing CSV file
            )